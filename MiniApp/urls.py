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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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


@csrf_exempt  # Убираем CSRF проверку для упрощения
def register_user(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        username = request.POST.get('username')

        if telegram_id and username:
            # Проверка, есть ли пользователь с таким telegram_id
            profile, created = Profile.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={'username': username}
            )
            if created:
                return JsonResponse({'status': 'success', 'message': 'User registered'})
            else:
                return JsonResponse({'status': 'success', 'message': 'User already exists'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', profile_view, name='profiles'),
    path('', lessons_view, name='lessons'),
    path('lesson/', lesson_view, name='lesson'),
    path('register_user/', register_user, name='register_user'),
]



