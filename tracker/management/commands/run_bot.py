import telebot
from telebot import types
from django.core.management.base import BaseCommand
from django.conf import settings
from tracker.models import Product
from tracker.scraper import getRozetkaPrice


class Command(BaseCommand):
    help = 'Запускає Telegram-бота з кнопками та підтримкою багатьох користувачів'

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
        self.stdout.write(self.style.SUCCESS('🤖 Бот запущений з інтерактивним меню!'))

        def get_main_menu():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_list = types.KeyboardButton("📋 Мій список")
            btn_help = types.KeyboardButton("ℹ️ Довідка")
            markup.add(btn_list, btn_help)
            return markup

        # Обробка команд /start, /menu, /help
        @bot.message_handler(commands=['start', 'menu', 'help'])
        def send_welcome(message):
            bot.send_message(
                message.chat.id,
                "Привіт! Я твій Universal Price Tracker. 🛒\n\n"
                "🔹 Скинь мені посилання на товар з Розетки, і я почну стежити.\n"
                "🔹 Натискай кнопки нижче для керування.",
                reply_markup=get_main_menu()
            )
        @bot.message_handler(func=lambda message: message.text in ["📋 Мій список", "ℹ️ Довідка"])
        def handle_menu(message):
            if message.text == "📋 Мій список":
                products = Product.objects.filter(telegram_chat_id=message.chat.id)

                if not products.exists():
                    bot.send_message(message.chat.id, "Твій список поки що пустий. Скинь мені якесь посилання!")
                    return

                bot.send_message(message.chat.id, "📊 Твої товари на моніторингу:")

                for p in products:
                    inline_markup = types.InlineKeyboardMarkup()
                    delete_btn = types.InlineKeyboardButton("❌ Видалити", callback_data=f"delete_{p.id}")
                    inline_markup.add(delete_btn)

                    msg_text = f"📦 *{p.name}*\n💰 Поточна ціна: {p.currentPrice} грн\n🔗 [Відкрити на сайті]({p.url})"
                    bot.send_message(message.chat.id, msg_text, reply_markup=inline_markup, parse_mode="Markdown")

            elif message.text == "ℹ️ Довідка":
                bot.send_message(message.chat.id,
                                 "🤖 Я працюю автоматично. Коли ціна на доданий тобою товар зміниться, я надішлю сповіщення.")

        @bot.message_handler(func=lambda message: True)
        def handle_links(message):
            text = message.text
            if 'rozetka.com.ua' in text:
                bot.reply_to(message, "⏳ Перевіряю посилання та ціну...")
                price = getRozetkaPrice(text)

                if price:
                    product, created = Product.objects.get_or_create(
                        telegram_chat_id=message.chat.id,
                        url=text,
                        defaults={'name': 'Товар з Telegram', 'currentPrice': price}
                    )

                    if created:
                        bot.send_message(message.chat.id,
                                         f"✅ Додано!\nПоточна ціна: {price} грн. Я дам знати, якщо вона зміниться.",
                                         reply_markup=get_main_menu())
                    else:
                        bot.send_message(message.chat.id,
                                         f"⚠️ Ти вже стежиш за цим товаром!\nЦіна: {product.currentPrice} грн.")
                else:
                    bot.send_message(message.chat.id, "❌ Не вдалося отримати ціну. Перевір посилання.")
            else:
                bot.send_message(message.chat.id, "🤔 Скинь посилання на Розетку або скористайся кнопками меню.",
                                 reply_markup=get_main_menu())

        @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
        def delete_callback(call):
            product_id = call.data.split('_')[1]
            try:
                product = Product.objects.get(id=product_id, telegram_chat_id=call.message.chat.id)
                product.delete()
                bot.answer_callback_query(call.id, "Товар видалено!")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="❌ Цей товар було видалено з твого трекеру.")
            except Product.DoesNotExist:
                bot.answer_callback_query(call.id, "Товар вже видалено.")

        bot.infinity_polling()