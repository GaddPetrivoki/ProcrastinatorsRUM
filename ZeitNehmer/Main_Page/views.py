from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<h1> Zeit Nehmer Worflow Manager <h1>') #Temporary html WebApp name
