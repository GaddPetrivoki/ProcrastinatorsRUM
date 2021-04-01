from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'Main_Page/home.html', {'title': 'Home'})

def login_Page(request):
   return render(request, 'Main_Page/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('Main-Page')
    else:
        form = UserCreationForm()

    return render(request, 'Main_Page/register.html', {'form': form})