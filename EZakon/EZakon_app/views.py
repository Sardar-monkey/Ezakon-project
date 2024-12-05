from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUser

from django.http import JsonResponse
import openai
import json

def main_page(request):
    return render(request, "./main.html")

def chat_page(request):
    return render(request, "./chat_ai.html")

def all_laws_page(request):
    return render(request, "./all_laws.html")

def laws_desc_page(request):
    return render(request, "./laws_desc.html")

def profile_page(request):
    return render(request, "./profile.html")

def lawyers_page(request):
    return render(request, "./lawers.html")

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

    return render(request, "./sign_up.html", {'form' : form})

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

    return render(request, "./login.html", {'form' : form})

def logout_act(request):
    logout(request)
    return redirect("main_page")

def sorry(request):
    return render(request, "./sorry.html")
# Login and SIGN UP



# Chat with AI
# Укажите свой API-ключ

def chat_with_ai(request):
    if request.method == 'POST':
        # Читаем данные, отправленные фронтендом
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Отправляем сообщение в OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Используемая модель
                messages=[
                    {"role": "system", "content": "Ты проффесиональный юрист помощник и отвечаешь только на вопросы связанные с законон"},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=150,
                temperature=0.7,
            )

            # Извлекаем ответ от OpenAI
            bot_reply = response['choices'][0]['message']['content']
            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            return JsonResponse({'reply': str(e)}, status=500)

# Chat with AI