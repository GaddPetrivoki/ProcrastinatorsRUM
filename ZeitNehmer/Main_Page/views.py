from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request, 'Main_Page/home.html', {'title': 'Home'})

def login_Page(request):
   return render(request, 'Main_Page/login.html')

def register(request):
    form = UserCreationForm()
    return render(request, 'Main_Page/register.html', {'form': form})