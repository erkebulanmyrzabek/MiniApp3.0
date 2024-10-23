"""
URL configuration for MiniApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Course.models import Profile
from django.shortcuts import render

def profile_view(request):
    # Получение всех профилей
    profiles = Profile.objects.all()
    return render(request, 'profile.html', {'profiles': profiles})

def lessons_view(request):
    username = Profile.objects.all()[0].username
    coin = Profile.objects.all()[0].coin
    return render(request, 'lessons.html', {'username': username, 'coin': coin})

def lesson_view(request):
    username = Profile.objects.all()
    coin = Profile.objects.all()[0].coin
    return render(request, 'lesson.html', {'username': username, 'coin': coin})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', profile_view, name='profiles'),
    path('', lessons_view, name='lessons'),
    path('lesson/', lesson_view, name='lesson'),
]



