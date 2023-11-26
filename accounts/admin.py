from django.contrib import admin

from accounts.models import User


# Register your models here.
@admin.register(User)
class BoardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "access_key",
        "secret_key",
        "bot_token",
    ]
    list_display_links = [
        "username",
    ]
    list_per_page = 10
