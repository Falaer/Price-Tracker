from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Назва товару")
    url = models.URLField(unique=True, verbose_name="Посилання на товар")
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Поточна ціна")
    desiredPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Бажана ціна")
    lastChecked = models.DateTimeField(auto_now=True, verbose_name="Останнє оновлення")

    def __str__(self):
        return self.name
