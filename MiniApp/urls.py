from django.contrib import admin
from django.contrib.sites import requests
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
    profiles = Profile.objects.all()
    return render(request, 'temp_files/profile.html', {'profiles': profiles})

#@csrf_exempt
# def lessons_view(request):
#     telegram_id = request.GET.get('telegram_id')
#
#     if telegram_id:
#         profile = get_object_or_404(Profile, telegram_id=telegram_id)
#         username = profile.username
#         coin = profile.coin
#         return render(request, 'temp_files/lessons.html', {'username': username, 'coin': coin})
#     else:
#         return JsonResponse({'error': 'Telegram ID not provided'}, status=400)
@csrf_exempt
def lesson_view(request):
    telegram_id = request.GET.get('telegram_id')

    if telegram_id:
        profile = get_object_or_404(Profile, telegram_id=telegram_id)
        username = profile.username
        coin = profile.coin
        return render(request, 'lesson.html', {'username': username, 'coin': coin})
    else:
        return JsonResponse({'error': 'Telegram ID not provided'}, status=400)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        username = request.POST.get('username')

        if telegram_id and username:
            profile, created = Profile.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={'username': username}
            )
            if created:

                return JsonResponse({'status': 'success', 'message': 'User registered'})
            else:
                return JsonResponse({'status': 'success', 'message': 'User already exists'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
# @csrf_exempt
# def city_view(request):
#     telegram_id = request.GET.get('telegram_id')
#
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

        return render(request, 'home.html', {'username': username, 'coin': coin})
    else:
        return render(request, 'error.html', {'error': 'Telegram ID not provided'})


def test_view(request):
    telegram_id = request.GET.get('telegram_id')
    if telegram_id:
        profile = get_object_or_404(Profile, telegram_id=telegram_id)
        username = profile.username
        coin = profile.coin
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
                profile.coin += coins_to_add
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
    profile = get_object_or_404(Profile, telegram_id=telegram_id)
    username = request.GET.get('username')

    # Ищем пользователя по telegram_id
    if telegram_id or username:
        username = profile.username
        coin = profile.coin

        building1_purchased = profile.building1_purchased
        building2_purchased = profile.building2_purchased
        building3_purchased = profile.building3_purchased
        building4_purchased = profile.building4_purchased
        # Передаем данные в шаблон
    return render(request, 'city.html', {'username': username, 'coin': coin, 'building1_purchased': building1_purchased, 'building2_purchased': building2_purchased, 'building3_purchased': building3_purchased, 'building4_purchased': building4_purchased, 'telegram_id': telegram_id})


@csrf_exempt
def buy_building(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        telegram_id = data.get('telegram_id')
        building = data.get('building')

        # Получаем профиль пользователя
        profile = get_object_or_404(Profile, telegram_id=telegram_id)

        if building == 1 :
            # Обновляем статус первого здания
            profile.building1_purchased = True
            profile.save()
            return JsonResponse({'status': 'success'})
        elif building == 2 :
            # Обновляем статус второго здания, если нужно
            profile.building2_purchased = True
            profile.save()
            return JsonResponse({'status': 'success'})
        # Можно добавить обработку для других зданий

        return JsonResponse({'status': 'error', 'message': 'Building already purchased or invalid request'})

chatgpt_api_key = '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'
chatgpt_url = "https://api.openai.com/v1/chat/completions"

from django.shortcuts import render

def ai_chat_view(request):
    # Получаем параметры из запроса (например, имя пользователя и количество коинов)
    username = request.GET.get('username', 'User')
    coin = request.GET.get('coin', 0)
    telegram_id = request.GET.get('telegram_id', '')

    # Передаем данные в шаблон
    return render(request, 'ai.html', {
        'username': username,
        'coin': coin,
        'telegram_id': telegram_id,
    })

# @csrf_exempt
# def send_message(request):
#     logger.info(f"Received request method: {request.method}")  # Log request method
#
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             logger.info(f"Received data: {data}")  # Log received data
#
#             user_message = data.get('message')
#
#             if not user_message:
#                 return JsonResponse({'error': 'Message not provided'}, status=400)
#
#             # ChatGPT API interaction code here...
#             chatgpt_params = {
#                 "model": "gpt-4o-2024-05-13",
#                 "messages": [
#                     {"role": "system", "content": "You are a helpful assistant named AI_Zhan. Respond in Kazakh."},
#                     {"role": "user", "content": user_message}
#                 ]
#             }
#
#             chatgpt_headers = {
#                 "Authorization": f"Bearer {chatgpt_api_key}",
#                 "Content-Type": "application/json"
#             }
#
#             chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_params)
#             chatgpt_response.raise_for_status()
#
#             chatgpt_result = chatgpt_response.json()
#             bot_response = chatgpt_result['choices'][0]['message']['content']
#
#             return JsonResponse({'response': bot_response})
#
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Request to ChatGPT failed: {e}")  # Log error
#             return JsonResponse({'error': f"Request failed: {e}"}, status=500)
#     else:
#         logger.warning("Invalid request method")  # Log invalid request method
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


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
    path('buy_building/', buy_building, name='buy_building'),
    path('ask_ai/', ai_chat_view, name='ask_ai'),
]



