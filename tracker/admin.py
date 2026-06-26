from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_chat_id', 'currentPrice', 'desiredPrice', 'last_checked')