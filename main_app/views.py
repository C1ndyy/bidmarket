from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'accounts/login.html')

def signup(request):
    return render(request, 'accounts/signup.html')