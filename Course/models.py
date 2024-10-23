from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.TextField(unique=True, verbose_name="Имя в телеграмме")
    telegram_id = models.TextField(unique=True, verbose_name="ID в телеграмме")
    coin = models.IntegerField(default=0, verbose_name="Кол-во коинов")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.username