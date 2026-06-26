from django.db import models

class Product(models.Model):
    telegram_chat_id = models.CharField(max_length=50, verbose_name="ID чату Telegram")
    name = models.CharField(max_length=255, verbose_name="Назва товару")
    url = models.URLField(verbose_name="Посилання на товар")
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Поточна ціна")
    desiredPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Бажана ціна")
    last_checked = models.DateTimeField(auto_now=True, verbose_name="Останнє оновлення")

    class Meta:
        unique_together = ('telegram_chat_id', 'url')
    def __str__(self):
        return f"{self.name} (Chat: {self.telegram_chat_id})"