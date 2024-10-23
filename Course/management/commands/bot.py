from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from Course.models import Profile
from asgiref.sync import sync_to_async
from django.conf import settings

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
            username = message.from_user.username or "anonymous"

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

        # Запуск бота
        executor.start_polling(dp, skip_updates=True)
