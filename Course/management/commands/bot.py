from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
from Course.models import Profile
from asgiref.sync import sync_to_async
from django.conf import settings
import requests

# Инициализация бота
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)

class Command(BaseCommand):
    help = "Запуск Telegram бота"

    def handle(self, *args, **kwargs):
        # Обработчик команды /start
        @dp.message_handler(commands=['start'])
        async def start_command(message: types.Message):
            telegram_id = message.from_user.id
            username = message.from_user.username or "anonymous"  # Убедитесь, что username не пустой

            # Проверка в базе данных, существует ли уже пользователь
            profile_exists = await sync_to_async(Profile.objects.filter(telegram_id=telegram_id).exists)()

            if not profile_exists:
                # Сохранение данных пользователя в базу
                await sync_to_async(Profile.objects.create)(
                    telegram_id=telegram_id, username=username
                )
                await message.answer(f"Привет, {username}! Ты успешно зарегистрирован.")
            else:
                await message.answer("Ты уже зарегистрирован!")

            # Создаем кнопку для мини-приложения
            web_app_url = f"https://3820-185-107-174-22.ngrok-free.app/?telegram_id={telegram_id}"  # URL мини-приложения с параметром
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url=web_app_url))
            markup.add(button)

            # Отправляем сообщение с кнопкой
            await message.answer("Нажмите на кнопку, чтобы открыть наш сайт как мини-приложение:", reply_markup=markup)

        # Запуск бота
        executor.start_polling(dp, skip_updates=True)
