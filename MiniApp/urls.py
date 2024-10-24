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
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json
@csrf_exempt
def profile_view(request):
    # Получение всех профилей
    profiles = Profile.objects.all()
    return render(request, 'temp_files/profile.html', {'profiles': profiles})
#@csrf_exempt
# def lessons_view(request):
#     # Получаем telegram_id из GET параметров
#     telegram_id = request.GET.get('telegram_id')
#
#     # Ищем пользователя по telegram_id
#     if telegram_id:
#         profile = get_object_or_404(Profile, telegram_id=telegram_id)
#         username = profile.username
#         coin = profile.coin
#         return render(request, 'temp_files/lessons.html', {'username': username, 'coin': coin})
#     else:
#         return JsonResponse({'error': 'Telegram ID not provided'}, status=400)
@csrf_exempt
def lesson_view(request):
    # Получаем telegram_id из GET параметров
    telegram_id = request.GET.get('telegram_id')

    # Ищем пользователя по telegram_id
    if telegram_id:
        profile = get_object_or_404(Profile, telegram_id=telegram_id)
        username = profile.username
        coin = profile.coin
        return render(request, 'lesson.html', {'username': username, 'coin': coin})
    else:
        return JsonResponse({'error': 'Telegram ID not provided'}, status=400)

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
# @csrf_exempt
# def city_view(request):
#     telegram_id = request.GET.get('telegram_id')
#
#     # Ищем пользователя по telegram_id
#     if telegram_id:
#         profile = get_object_or_404(Profile, telegram_id=telegram_id)
#         username = profile.username
#         coin = profile.coin
#         return render(request, 'temp_files/city.html', {'username': username, 'coin': coin})
#     else:
#         return JsonResponse({'error': 'Telegram ID not provided'}, status=400)
# @csrf_exempt
# def test_view(request):
#     telegram_id = request.GET.get('telegram_id')
#     if telegram_id:
#         profile = get_object_or_404(Profile, telegram_id=telegram_id)
#         username = profile.username
#         coin = profile.coin
#         return render(request, 'temp_files/test.html', {'username': username, 'coin': coin})
#     else:
#         return JsonResponse({'error': 'Telegram ID not provided'}, status=400)


def home_view(request):
    telegram_id = request.GET.get('telegram_id')
    username = request.GET.get('username')

    # Ищем пользователя по telegram_id
    if telegram_id or username:
        profile = get_object_or_404(Profile, telegram_id=telegram_id)
        username = profile.username
        coin = profile.coin

        # Передаем данные в шаблон
        return render(request, 'home.html', {'username': username, 'coin': coin})
    else:
        return render(request, 'error.html', {'error': 'Telegram ID not provided'})


def test_view(request):
    # Получаем username и coin из запроса (или профиля)
    telegram_id = request.GET.get('telegram_id')
    if telegram_id:
        profile = get_object_or_404(Profile, telegram_id=telegram_id)
        username = profile.username
        coin = profile.coin
    # Передаем данные в шаблон
        return render(request, 'test.html', {'username': username, 'coin': coin, 'profile' : profile, 'telegram_id' : telegram_id})
    else:
        return render(request, 'error.html')

@csrf_exempt
def update_coins(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            coins_to_add = data.get('coins')

            if telegram_id and coins_to_add:
                profile = Profile.objects.get(telegram_id=telegram_id)
                profile.coin += coins_to_add  # Добавляем количество коинов
                profile.save()

                return JsonResponse({'status': 'success', 'new_balance': profile.coin})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def city_view(request):
    telegram_id = request.GET.get('telegram_id')

    # Проверяем наличие telegram_id
    if telegram_id:
        profile = get_object_or_404(Profile, telegram_id=telegram_id)
        username = profile.username
        coin = profile.coin

        # Рендерим шаблон city.html с передачей данных
        return render(request, 'city.html', {'username': username, 'coin': coin, 'telegram_id': telegram_id})
    else:
        return render(request, 'error.html', {'error': 'Telegram ID not provided'})
urlpatterns = [
    path('admin/', admin.site.urls),
   #path('profiles/', profile_view, name='profiles'),
    #path('lessons/', lessons_view, name='lessons'),
    path('lesson/', lesson_view, name='lesson'),
    path('register_user/', register_user, name='register_user'),
   # path('city/', city_view, name='city'),
    #path('test/', test_view, name='test'),
    path('', home_view, name='home'),
    path('test/', test_view, name='test'),
    path('update_coins/', update_coins, name='update_coins'),
    path('city/', city_view, name='city'),
]



