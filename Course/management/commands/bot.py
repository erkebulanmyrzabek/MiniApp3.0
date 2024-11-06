from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
from Course.models import Profile
from asgiref.sync import sync_to_async
from django.conf import settings
import requests

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)

class Command(BaseCommand):
    help = "Запуск Telegram бота"

    def handle(self, *args, **kwargs):
        @dp.message_handler(commands=['start'])
        async def start_command(message: types.Message):
            telegram_id = message.from_user.id
            username = message.from_user.username or "anonymous"

            profile_exists = await sync_to_async(Profile.objects.filter(telegram_id=telegram_id).exists)()

            if not profile_exists:
                await sync_to_async(Profile.objects.create)(
                    telegram_id=telegram_id, username=username
                )
                await message.answer(f"Привет, {username}! Ты успешно зарегистрирован.")
            else:
                await message.answer("Ты уже зарегистрирован!")

            web_app_url = f"https://25cf-2a0d-b201-a001-d033-bda6-630a-81ec-b4e5.ngrok-free.app/?telegram_id={telegram_id}"
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url=web_app_url))
            markup.add(button)

            await message.answer("Нажмите на кнопку, чтобы открыть наш сайт как мини-приложение:", reply_markup=markup)

        executor.start_polling(dp, skip_updates=True)
