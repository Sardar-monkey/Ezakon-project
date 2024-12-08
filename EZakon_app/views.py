from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUser, CommentForm
from .models import Lawyer, Comment
from django.http import JsonResponse
import openai
import json

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
    context = {'lawyers': lawyers}
    return render(request, "lawers.html", context)

def lawyer_profile_page(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    context = {'lawyer': lawyer}
    return render(request, "LawyerProfile.html", context)

def comments_page(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    comments = Comment.objects.filter(lawyer=lawyer).order_by('-created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.lawyer = lawyer
                comment.author = request.user
                comment.save()
                # Обновляем количество комментариев в модели Lawyer
                lawyer.com = comments.count() + 1  # +1 для нового комментария
                lawyer.save()
                return redirect('comments_page', pk=lawyer.pk)
        else:
            # Перенаправление на страницу входа, если пользователь не аутентифицирован
            return redirect('login_view')
    else:
        form = CommentForm()
    
    context = {
        'lawyer': lawyer,
        'comments': comments,
        'form': form,
    }
    return render(request, "comments.html", context)

# Login and SIGN UP
def sign_up(request):
    if request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = NewUser()
    return render(request, "sign_up.html", {'form' : form})

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
    return render(request, "login.html", {'form' : form})

def logout_act(request):
    logout(request)
    return redirect("main_page")

def sorry(request):
    return render(request, "sorry.html")

# Chat with AI
openai.api_key = "Your_Api_Key"

def chat_with_ai(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты профессиональный юрист помощник и отвечаешь только на вопросы связанные с законодательством"},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=150,
                temperature=0.7,
            )

            bot_reply = response['choices'][0]['message']['content']
            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            return JsonResponse({'reply': str(e)}, status=500)
