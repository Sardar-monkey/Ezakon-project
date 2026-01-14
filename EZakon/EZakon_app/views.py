import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUser, CommentForm, LawSearchForm, LawCommentForm
from .models import Lawyer, Comment, Law, LawComment, FavoriteLaw, LawHistory
from django.http import JsonResponse
from decouple import config
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import re
from django.utils.html import escape
from difflib import SequenceMatcher

# Импортируем API с обработкой ошибок
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("WARNING: google-generativeai не установлена. Установите: pip install google-generativeai")

# Конфигурируем API ключ с обработкой ошибок
GEMINI_API_KEY = None
if GEMINI_AVAILABLE:
    try:
        GEMINI_API_KEY = config("GEMINI_API_KEY", default=None)
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
        else:
            print("WARNING: GEMINI_API_KEY не найден в .env файле")
    except Exception as e:
        print(f"ERROR: Ошибка при конфигурации API: {e}")


def main_page(request):
    return render(request, "main.html")


def chat_page(request):
    return render(request, "chat_ai.html")


def all_laws_page(request):
    form = LawSearchForm(request.GET)
    laws = Law.objects.filter(is_active=True)

    if form.is_valid():
        query = form.cleaned_data.get("query", "")
        category = form.cleaned_data.get("category", "")
        status = form.cleaned_data.get("status", "")
        is_active = form.cleaned_data.get("is_active", "")
        sort_by = form.cleaned_data.get("sort_by", "-date_published")

        if query:
            laws = laws.filter(
                Q(title__icontains=query)
                | Q(number__icontains=query)
                | Q(description__icontains=query)
                | Q(full_text__icontains=query)
            )

        if category:
            laws = laws.filter(category=category)

        if status:
            laws = laws.filter(status=status)

        if is_active == "true":
            laws = laws.filter(is_active=True)

        if sort_by:
            laws = laws.order_by(sort_by)
    else:
        laws = laws.order_by("-date_published")

    paginator = Paginator(laws, 10)
    page_number = request.GET.get("page")

    try:
        laws_page = paginator.page(page_number)
    except PageNotAnInteger:
        laws_page = paginator.page(1)
    except EmptyPage:
        laws_page = paginator.page(paginator.num_pages)

    total_laws = Law.objects.count()
    categories = dict(Law.CATEGORY_CHOICES)

    context = {
        "laws": laws_page,
        "form": form,
        "total_laws": total_laws,
        "categories": categories,
        "query": request.GET.get("query", ""),
    }

    return render(request, "all_laws.html", context)


def law_detail_page(request, slug):

    law = get_object_or_404(Law, slug=slug)

    law.increment_views()

    history = law.history.all()[:5]

    comments = law.law_comments.all()

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteLaw.objects.filter(user=request.user, law=law).exists()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = LawCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.law = law
                comment.author = request.user
                comment.save()
                return redirect("law_detail", slug=law.slug)
        else:
            return redirect("login_view")
    else:
        form = LawCommentForm()

    context = {
        "law": law,
        "history": history,
        "comments": comments,
        "form": form,
        "is_favorited": is_favorited,
    }

    return render(request, "law_detail.html", context)


def laws_desc_page(request):
    return render(request, "laws_desc.html")


def profile_page(request):
    return render(request, "profile.html")


def lawyers_page(request):
    lawyers = Lawyer.objects.all()
    context = {"lawyers": lawyers}
    return render(request, "lawers.html", context)


def lawyer_profile_page(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    context = {"lawyer": lawyer}
    return render(request, "LawyerProfile.html", context)


def comments_page(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    comments = Comment.objects.filter(lawyer=lawyer).order_by("?")

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.lawyer = lawyer
                comment.author = request.user
                comment.save()
                return redirect("comments_page", pk=lawyer.pk)
        else:
            return redirect("login_view")
    else:
        form = CommentForm()

    context = {
        "lawyer": lawyer,
        "comments": comments,
        "form": form,
    }
    return render(request, "comments.html", context)


@login_required(login_url="login_view")
def add_favorite_law(request, slug):
    """Добавить закон в избранное"""
    law = get_object_or_404(Law, slug=slug)

    favorite, created = FavoriteLaw.objects.get_or_create(user=request.user, law=law)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "is_favorited": created,
                "message": (
                    "Добавлено в избранное" if created else "Удалено из избранного"
                ),
            }
        )

    return redirect("law_detail", slug=law.slug)


@login_required(login_url="login_view")
def remove_favorite_law(request, slug):

    law = get_object_or_404(Law, slug=slug)

    FavoriteLaw.objects.filter(user=request.user, law=law).delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {"success": True, "is_favorited": False, "message": "Удалено из избранного"}
        )

    return redirect("law_detail", slug=law.slug)


@login_required(login_url="login_view")
def favorite_laws_page(request):

    favorites = FavoriteLaw.objects.filter(user=request.user).select_related("law")
    laws = [fav.law for fav in favorites]

    context = {
        "laws": laws,
        "title": "Мои избранные законы",
    }

    return render(request, "favorite_laws.html", context)


def sign_up(request):
    if request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main_page")
    else:
        form = NewUser()
    return render(request, "sign_up.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main_page")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_act(request):
    logout(request)
    return redirect("main_page")


def sorry(request):
    return render(request, "sorry.html")


def chat_with_ai(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "error": "Требуется вход в аккаунт",
                    "reply": ["Пожалуйста, войдите в аккаунт для использования чата"],
                },
                status=401,
            )

        if not GEMINI_AVAILABLE:
            return JsonResponse(
                {
                    "error": "API недоступен",
                    "reply": ["Библиотека google-generativeai не установлена. Свяжитесь с администратором."],
                },
                status=503,
            )

        if not GEMINI_API_KEY:
            return JsonResponse(
                {
                    "error": "API не сконфигурирован",
                    "reply": ["API ключ не найден. Свяжитесь с администратором."],
                },
                status=503,
            )

        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse(
                    {
                        "error": "Сообщение пусто",
                        "reply": ["Пожалуйста, введите сообщение"],
                    },
                    status=400,
                )

            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                full_prompt = f"Ты профессиональный юрист помощник и отвечаешь только на вопросы связанные с законодательством.\n\nПользователь: {user_message}\nОтвет:"
                response = model.generate_content(full_prompt)

                bot_reply_text = response.text
                bot_reply_text = re.sub(r"\*", "", bot_reply_text)
                bot_reply_list = re.split(r"\n(?=\d+\.\s)", bot_reply_text)
                bot_reply_list = [item.strip() for item in bot_reply_list if item.strip()]

                return JsonResponse({"reply": bot_reply_list})
            
            except Exception as api_error:
                print(f"Error with Gemini API: {api_error}")
                error_msg = str(api_error)
                
                # Детальная информация об ошибке
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    return JsonResponse(
                        {
                            "error": "Ошибка аутентификации API",
                            "reply": ["Неверный или истекший API ключ. Свяжитесь с администратором."],
                        },
                        status=503,
                    )
                elif "rate" in error_msg.lower():
                    return JsonResponse(
                        {
                            "error": "Превышен лимит запросов",
                            "reply": ["Слишком много запросов. Попробуйте позже."],
                        },
                        status=429,
                    )
                else:
                    return JsonResponse(
                        {
                            "error": "Ошибка при обработке запроса",
                            "reply": ["Временная ошибка сервиса. Попробуйте позже."],
                        },
                        status=503,
                    )

        except json.JSONDecodeError:
            print("JSON decode error")
            return JsonResponse(
                {
                    "error": "Ошибка формата данных",
                    "reply": ["Произошла ошибка при обработке данных"],
                },
                status=400,
            )

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)
