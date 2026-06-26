from django.core.management.base import BaseCommand
from tracker.models import Product
from tracker.scraper import getRozetkaPrice


class Command(BaseCommand):
    help = 'Автоматично оновлює ціни для всіх товарів у базі даних'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        self.stdout.write(f"Знайдено товарів у базі: {products.count()}")

        for product in products:
            self.stdout.write(f"Перевіряю ціну для: {product.name}...")

            if 'rozetka.com.ua' in product.url:
                new_price = getRozetkaPrice(product.url)

                if new_price:
                    product.current_price = new_price
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f"Успіх! Нова ціна: {new_price} грн"))
                else:
                    self.stdout.write(self.style.ERROR(f"Не вдалося отримати ціну для {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Парсер для цього магазину ще не написаний, пропускаю."))