from django.shortcuts import render

def temp(request):
    return render(request, "./base.html")