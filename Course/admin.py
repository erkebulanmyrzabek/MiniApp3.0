from django.contrib import admin

from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'telegram_id', 'coin', 'building1_purchased', 'building2_purchased', 'building3_purchased', 'building4_purchased')

