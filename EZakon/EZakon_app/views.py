from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUser, CommentForm
from .models import Lawyer, Comment
from django.http import JsonResponse
from decouple import config
import google.generativeai as genai
import json
import re 


def main_page(request):
    return render(request, "main.html")


def chat_page(request):
    return render(request, "chat_ai.html")


def all_laws_page(request):
    return render(request, "all_laws.html")


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


# Login and SIGN UP
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


# иишка добавлена
genai.configure(api_key=config('GEMINI_API_KEY'))


def chat_with_ai(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            full_prompt = f"Ты профессиональный юрист помощник и отвечаешь только на вопросы связанные с законодательством.\n\nПользователь: {user_message}\nОтвет:"
            response = model.generate_content(full_prompt)

            bot_reply_text = response.text
            bot_reply_text = re.sub(r"\*", "", bot_reply_text)
            bot_reply_list = re.split(r"\n(?=\d+\.\s)", bot_reply_text)
            bot_reply_list = [item.strip() for item in bot_reply_list if item.strip()]

            return JsonResponse({"reply": bot_reply_list})

        except Exception as e:
            print(f"Error with Gemini API: {e}")
            return JsonResponse(
                {"reply": [f"Произошла ошибка при обращении к AI: {str(e)}"]},
                status=500,
            )

