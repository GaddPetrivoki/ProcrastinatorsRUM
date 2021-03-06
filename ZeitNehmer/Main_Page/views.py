from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'Main_Page/home.html', {'title': 'Home'})

def login_Page(request):
   return render(request, 'Main_Page/login.html')