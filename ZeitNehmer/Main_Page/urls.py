from django.urls import path
from . import views


#URL patterns of Main Page

urlpatterns = [
    path('', views.home, name='Main-Page'),
    path('register/', views.register, name='Register-Page')
]