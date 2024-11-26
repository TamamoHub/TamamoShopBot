import os
import telebot
from telebot import types
import random
from collections import defaultdict
from datetime import datetime, timedelta
import requests
import time
import threading


bot = telebot.TeleBot('TELEGRAM_BOT_TOKEN')

products = [{
    "name": "Apple iMac 27",
    "price": "₴69,999",
    "discount": "Up to 35% off",
    "rating": 4.8,
    "reviews": 455,
    "delivery": "Fast Delivery",
    "emoji": "💻",
    "specs": {
        "display": "27-inch Retina 5K",
        "processor": "10th-generation Intel Core i5",
        "memory": "8GB RAM",
        "storage": "256GB SSD"
    }
}, {
    "name": "Apple iPhone 15 Pro Max",
    "price": "₴49,999",
    "discount": "Up to 15% off",
    "rating": 4.9,
    "reviews": 1023,
    "delivery": "Best Seller",
    "emoji": "📱",
    "specs": {
        "display": "6.7-inch Super Retina XDR",
        "processor": "A17 Pro chip",
        "camera": "Pro camera system",
        "battery": "Up to 29 hours video playback"
    }
}, {
    "name": "iPad Pro 13-Inch",
    "price": "₴33,999",
    "discount": "Up to 35% off",
    "rating": 4.7,
    "reviews": 789,
    "delivery": "Shipping Today",
    "emoji": "📱",
    "specs": {
        "display": "13-inch Liquid Retina XDR",
        "processor": "M2 chip",
        "camera": "12MP Ultra Wide front camera",
        "connectivity": "5G capable"
    }
}, {
    "name": "PlayStation 5",
    "price": "₴20,999",
    "discount": "Up to 10% off",
    "rating": 4.5,
    "reviews": 364,
    "delivery": "Fast Delivery",
    "emoji": "🎮",
    "specs": {
        "processor": "AMD Ryzen Zen 2",
        "gpu": "RDNA 2-based graphics engine",
        "memory": "16GB GDDR6",
        "storage": "825GB SSD"
    }
}, {
    "name": "Xbox Series X",
    "price": "₴20,999",
    "discount": "Up to 10% off",
    "rating": 4.5,
    "reviews": 364,
    "delivery": "Best Seller",
    "emoji": "🎮",
    "specs": {
        "processor": "AMD Ryzen Zen 2",
        "gpu": "RDNA 2-based graphics engine",
        "memory": "16GB GDDR6",
        "storage": "1TB SSD"
    }
}, {
    "name": "Apple MacBook PRO",
    "price": "₴108,999",
    "discount": "Up to 5% off",
    "rating": 4.9,
    "reviews": 556,
    "delivery": "Fast Delivery",
    "emoji": "💻",
    "specs": {
        "display": "16-inch Retina",
        "processor": "M1 Pro chip",
        "memory": "16GB RAM",
        "storage": "512GB SSD"
    }
}, {
    "name": "Apple Watch SE [GPS 40mm]",
    "price": "₴29,999",
    "discount": "Up to 20% off",
    "rating": 4.6,
    "reviews": 542,
    "delivery": "Fast Delivery",
    "emoji": "⌚",
    "specs": {
        "display": "1.57-inch Retina OLED",
        "processor": "S5 chip",
        "battery": "Up to 18 hours",
        "connectivity": "GPS"
    }
}]

orders = {}
comparison_dict = {}
subscriptions = {}
loyalty_points = {}
user_reviews = {}
product_ratings = {}
active_discounts = {} 
support_user_id = 7501490975
rewards = {
    "discount_5": {"name": "5% знижка на наступну покупку", "cost": 500, "type": "discount", "value": 5},
    "discount_10": {"name": "10% знижка на наступну покупку", "cost": 1000, "type": "discount", "value": 10},
    "free_accessory": {"name": "Ексклюзивний аксесуар у подарунок", "cost": 2000, "type": "gift"},
    "engraving": {"name": "Індивідуальне гравірування на аксесуарах", "cost": 3000, "type": "service"},
    "early_access": {"name": "Доступ до новинок на день раніше", "cost": 5000, "type": "privilege"},
    "virtual_tour": {"name": "Віртуальна екскурсія Apple Store в Каліфорнії з гідом", "cost": 10000, "type": "experience"},
    "home_setup": {"name": "Візит техніка для налаштування техніки вдома", "cost": 12000, "type": "service"},
    "event_raffle": {"name": "Участь у розіграші на запрошення на офіційну презентацію Apple", "cost": 15000, "type": "raffle"},
    "subscription": {"name": "Річна підписка на Apple Music або Apple TV+", "cost": 20000, "type": "subscription"},
    "insider_club": {"name": "Членство в клубі 'Apple Insiders' з доступом до привілеїв та знижок", "cost": 30000, "type": "membership"}
}
promotions = {
    "NEWCLIENT10": {"discount": 10, "name": "Знижка на першу покупку"},
    "AUTUMN20": {"discount": 20, "name": "Осінній розпродаж"},
    "BLACKFRIDAY": {"discount": 30, "name": "Чорна п'ятниця"},
    "MARKETING": {"discount": 40, "name": "Інтернет-маркетинг"},
    "TAMASHOPBOT": {"discount": 50, "name": "Запуск бота"}
}
used_promo_codes = defaultdict(set)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    website_btn = types.KeyboardButton('🌐 Перейти на сайт')
    markup.add(website_btn)
    catalog_btn = types.KeyboardButton('📱 Каталог товарів')
    compare_btn = types.KeyboardButton('🔍 Порівняти товари')
    discounts_btn = types.KeyboardButton('💸 Знижки та акції')
    orders_btn = types.KeyboardButton('📦 Мої замовлення')
    subscribe_btn = types.KeyboardButton('🔔 Підписатися на оновлення')
    loyalty_btn = types.KeyboardButton('🎁 Програма лояльності')
    reviews_btn = types.KeyboardButton('⭐ Відгуки та рейтинги')
    support_btn = types.KeyboardButton('🛠️ Підтримка')
    share_btn = types.KeyboardButton('📢 Поділитися в соцмережах')
    panel_btn = types.KeyboardButton('🔒 Panel')
    markup.add(catalog_btn, compare_btn, discounts_btn, orders_btn,
               subscribe_btn, loyalty_btn, reviews_btn, support_btn, share_btn,
               panel_btn)
    bot.send_message(
        message.chat.id,
        "🍏 Вітаємо в TamaShop! 🎉\n\nОберіть опцію зі списку нижче: 👇",
        reply_markup=markup)
    
@bot.message_handler(func=lambda message: message.text == '🌐 Перейти на сайт')
def go_to_website(message):
    markup = types.InlineKeyboardMarkup()
    website_button = types.InlineKeyboardButton("Відвідати наш сайт", url="https://tamashop.vercel.app/")
    back_button = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
    markup.add(website_button, back_button)
    bot.send_message(message.chat.id, "Ласкаво просимо на наш сайт! Оберіть опцію:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🔒 Panel')
def handle_panel(message):
    user_id = message.from_user.id
    if user_id == 7501490975:
        bot.send_message(message.chat.id,
                         "Ви маєте доступ до панелі адміністратора.")
    else:
        bot.send_message(
            message.chat.id,
            "У вас немає доступу до панелі. Повертаємось до головного меню.")
        send_welcome(message)


@bot.message_handler(func=lambda message: message.text == '📱 Каталог товарів')
def show_products(message):
    markup = types.InlineKeyboardMarkup()
    for index, product in enumerate(products):
        button = types.InlineKeyboardButton(
            f"{product['emoji']} {product['name']} - {product['price']}",
            callback_data=f"product_{index}")
        markup.add(button)
    bot.send_message(message.chat.id,
                     "📦 Оберіть товар з нашого чудового асортименту: 🛍️",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def show_product_details(call):
    product_index = int(call.data.split('_')[1])
    product = products[product_index]

    markup = types.InlineKeyboardMarkup()
    buy_button = types.InlineKeyboardButton(
        "🛒 Купити", callback_data=f"buy_{product_index}")
    review_button = types.InlineKeyboardButton(
        "⭐ Залишити відгук", callback_data=f"leave_review_{product_index}")
    share_button = types.InlineKeyboardButton(
        "📢 Поділитися", callback_data=f"share_product_{product_index}")
    back_button = types.InlineKeyboardButton("🔙 Назад",
                                             callback_data="back_to_products")

    markup.add(buy_button, review_button, share_button, back_button)

    bot.edit_message_text(
        f"{product['emoji']} {product['name']}\n💰 Ціна: {product['price']}\n🏷️ Знижка: {product['discount']}\n⭐ Рейтинг: {product['rating']} ({product['reviews']} відгуків)\n🚚 Доставка: {product['delivery']}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('share_product_'))
def share_product(call):
    product_index = int(call.data.split('_')[2])
    product = products[product_index]

    share_text = f"""🚀 Вау! Погляньте на цей неймовірний товар у @TamaShop_Bot! 😍

{product['emoji']} {product['name']}
💰 Ціна: {product['price']}
🏷️ Знижка: {product['discount']}
⭐ Рейтинг: {product['rating']} ({product['reviews']} відгуків)

🛍️ Купуйте в TamaShop - найкрутішому магазині Apple техніки! 🍏✨
Приєднуйтесь до технологічної революції прямо зараз! 🚀🌟"""

    markup = types.InlineKeyboardMarkup()
    telegram_button = types.InlineKeyboardButton(
        "Telegram 📬",
        url=
        f"https://t.me/share/url?url=https://t.me/TamaShopBot&text={share_text}"
    )
    twitter_button = types.InlineKeyboardButton(
        "Twitter 🐦", url=f"https://twitter.com/intent/tweet?text={share_text}")
    facebook_button = types.InlineKeyboardButton(
        "Facebook 👥",
        url=
        f"https://www.facebook.com/sharer/sharer.php?u=https://t.me/TamaShopBot&quote={share_text}"
    )
    back_button = types.InlineKeyboardButton(
        "🔙 Назад", callback_data=f"product_{product_index}")

    markup.add(telegram_button, twitter_button, facebook_button, back_button)

    bot.edit_message_text("Оберіть соціальну мережу, щоб поділитися товаром:",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('leave_review_'))
def leave_review(call):
    product_index = int(call.data.split('_')[2])
    product = products[product_index]

    markup = types.InlineKeyboardMarkup()
    for i in range(1, 6):
        markup.add(
            types.InlineKeyboardButton(
                f"{i} ⭐", callback_data=f"rate_{product_index}_{i}"))

    bot.edit_message_text(f"Оцініть {product['emoji']} {product['name']}:",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)

    @bot.message_handler(
        func=lambda message: message.text == '🔍 Порівняти товари')
    def compare_products(message):
        comparison_dict[message.chat.id] = []
        markup = types.InlineKeyboardMarkup()
        for index, product in enumerate(products):
            button = types.InlineKeyboardButton(
                f"{product['emoji']} {product['name']}",
                callback_data=f"compare_{index}")
            markup.add(button)
        bot.send_message(message.chat.id,
                         "🔍 Оберіть перший товар для порівняння:",
                         reply_markup=markup)

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith('compare_'))
    def handle_compare(call):
        product_index = int(call.data.split('_')[1])
        chat_id = call.message.chat.id

        if chat_id not in comparison_dict:
            comparison_dict[chat_id] = []

        comparison_dict[chat_id].append(product_index)

        if len(comparison_dict[chat_id]) == 1:
            markup = types.InlineKeyboardMarkup()
            for index, product in enumerate(products):
                if index != product_index:
                    button = types.InlineKeyboardButton(
                        f"{product['emoji']} {product['name']}",
                        callback_data=f"compare_{index}")
                    markup.add(button)
            bot.edit_message_text(
                f"🔍 Порівняння: {products[product_index]['name']} з...",
                chat_id,
                call.message.message_id,
                reply_markup=markup)
        elif len(comparison_dict[chat_id]) == 2:
            show_comparison(call.message, comparison_dict[chat_id])
            comparison_dict[chat_id] = []

    def show_comparison(message, product_indices):
        first_product = products[product_indices[0]]
        second_product = products[product_indices[1]]

        comparison = f"🔍 Порівняння:\n\n"
        comparison += f"{first_product['emoji']} {first_product['name']} vs {second_product['emoji']} {second_product['name']}\n\n"

        comparison += f"💰 Ціна:\n"
        comparison += f"- {first_product['name']}: {first_product['price']}\n"
        comparison += f"- {second_product['name']}: {second_product['price']}\n\n"

        comparison += f"🏷️ Знижка:\n"
        comparison += f"- {first_product['name']}: {first_product['discount']}\n"
        comparison += f"- {second_product['name']}: {second_product['discount']}\n\n"

        comparison += f"⭐ Рейтинг:\n"
        comparison += f"- {first_product['name']}: {first_product['rating']} ({first_product['reviews']} відгуків)\n"
        comparison += f"- {second_product['name']}: {second_product['rating']} ({second_product['reviews']} відгуків)\n\n"

        comparison += f"🚚 Доставка:\n"
        comparison += f"- {first_product['name']}: {first_product['delivery']}\n"
        comparison += f"- {second_product['name']}: {second_product['delivery']}\n\n"

        comparison += f"📊 Характеристики:\n"
        all_specs = set(first_product['specs'].keys()) | set(
            second_product['specs'].keys())
        for spec in all_specs:
            comparison += f"{spec.capitalize()}:\n"
            comparison += f"- {first_product['name']}: {first_product['specs'].get(spec, 'N/A')}\n"
            comparison += f"- {second_product['name']}: {second_product['specs'].get(spec, 'N/A')}\n\n"

        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            "🔙 Назад до порівняння", callback_data="back_to_compare")
        markup.add(back_button)

        bot.edit_message_text(comparison,
                              message.chat.id,
                              message.message_id,
                              reply_markup=markup)

    @bot.callback_query_handler(
        func=lambda call: call.data == "back_to_compare")
    def back_to_compare(call):
        compare_products(call.message)


# Обробка кнопки "Назад" до списку продуктів
@bot.callback_query_handler(func=lambda call: call.data == "back_to_products")
def back_to_products(call):
    markup = types.InlineKeyboardMarkup()
    for index, product in enumerate(products):
        button = types.InlineKeyboardButton(
            f"{product['emoji']} {product['name']} - {product['price']}",
            callback_data=f"product_{index}")
        markup.add(button)
    bot.edit_message_text("📦 Оберіть товар з нашого чудового асортименту: 🛍️",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


# Обробка натискання кнопки "Купити"
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_purchase(call):
    try:
        product_index = int(call.data.split('_')[1])
        product = products[product_index]

        markup = types.InlineKeyboardMarkup()
        
        # Створюємо кнопки для доступних промокодів
        user_id = call.from_user.id
        for code, promo in promotions.items():
            if code not in used_promo_codes[user_id]:
                button_text = f"{code} ({promo['discount']}% знижки)"
                callback_data = f"apply_promo_{product_index}_{code}"
                markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        # Додаємо кнопку для знижки з програми лояльності, якщо вона є
        if user_id in active_discounts:
            loyalty_discount = active_discounts[user_id]
            button_text = f"Знижка з програми лояльності ({loyalty_discount}%)"
            callback_data = f"apply_loyalty_discount_{product_index}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        # Додаємо кнопку "Без промокоду"
        skip_promo_button = types.InlineKeyboardButton("Без промокоду", callback_data=f"skip_promo_{product_index}")
        markup.add(skip_promo_button)

        bot.edit_message_text(
            f"Виберіть промокод для покупки {product['emoji']} {product['name']} або продовжіть без знижки:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except (IndexError, ValueError):
        bot.send_message(
            call.message.chat.id,
            "❌ Ой! Виникла помилка. 😕 Будь ласка, спробуйте ще раз. 🔄")
        
@bot.callback_query_handler(func=lambda call: call.data.startswith('apply_loyalty_discount_'))
def apply_loyalty_discount(call):
    product_index = int(call.data.split('_')[3])  # Індекс продукту
    user_id = call.from_user.id
    
    if user_id in active_discounts:
        # Застосовуємо знижку з програми лояльності
        discount = active_discounts[user_id]
        complete_purchase(call.message, product_index, discount, promo_code=None)
    else:
        bot.answer_callback_query(call.id, "Знижка з програми лояльності недоступна.")



@bot.callback_query_handler(func=lambda call: call.data.startswith('apply_promo_'))
def apply_promo_code(call):
    data_parts = call.data.split('_')
    product_index = data_parts[2]  # Індекс продукту
    promo_code = "_".join(data_parts[3:])  # Залишок даних об'єднується в промокод
    user_id = call.from_user.id
    
    if promo_code in promotions and promo_code not in used_promo_codes[user_id]:
        discount = promotions[promo_code]["discount"]
        used_promo_codes[user_id].add(promo_code)
        complete_purchase(call.message, int(product_index), discount, promo_code)
    else:
        bot.answer_callback_query(call.id, "Цей промокод вже використаний або недійсний.")
        complete_purchase(call.message, int(product_index), 0, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith('skip_promo_'))
def skip_promo(call):
    product_index = int(call.data.split('_')[2])
    bot.answer_callback_query(call.id)
    complete_purchase(call.message, product_index, 0, None)

def complete_purchase(message, product_index, discount, promo_code):
    user_id = message.chat.id
    product = products[product_index]
    original_price = float(product['price'].replace('₴', '').replace(',', ''))
    
    # Перевіряємо, чи є у користувача активна знижка з програми лояльності
    loyalty_discount = active_discounts.get(user_id, 0)
    
    # Якщо є промокод і знижка з лояльності, поєднуємо їх
    total_discount = discount + loyalty_discount
    
    # Обмежуємо максимальну знижку, щоб не перевищувати 100%
    total_discount = min(total_discount, 100)
    
    # Розраховуємо кінцеву ціну
    discounted_price = original_price * (1 - total_discount / 100)
    
    # Зберігаємо замовлення
    if user_id not in orders:
        orders[user_id] = []
    orders[user_id].append(product)

    # Додаємо бали лояльності
    if user_id not in loyalty_points:
        loyalty_points[user_id] = 0
    loyalty_points[user_id] += int(discounted_price * 0.01)

    promo_info = f"Використаний промокод: {promo_code}\n" if promo_code else ""
    loyalty_info = f"Застосовано знижку {loyalty_discount}% від програми лояльності.\n" if loyalty_discount else ""

    # Видаляємо активну знижку після використання
    if user_id in active_discounts:
        del active_discounts[user_id]
    
    bot.send_message(
        message.chat.id,
        f"🎉 Вітаємо з покупкою {product['emoji']} {product['name']}!\n"
        f"Оригінальна ціна: ₴{original_price:.2f}\n"
        f"{promo_info}"
        f"{loyalty_info}"
        f"Знижка: {total_discount}%\n"
        f"Фінальна ціна: ₴{discounted_price:.2f}\n\n"
        f"Товар додано до ваших замовлень. 📦✨\n"
        f"Ви отримали {int(discounted_price * 0.01)} балів лояльності! 🎁"
    )


# Обробка натискання на кнопку "Порівняти товари"
@bot.message_handler(func=lambda message: message.text == '🔍 Порівняти товари')
def compare_products(message):
    comparison_dict[message.chat.id] = []  # Очищаємо попередній вибір
    markup = types.InlineKeyboardMarkup()
    for index, product in enumerate(products):
        button = types.InlineKeyboardButton(
            f"{product['emoji']} {product['name']}",
            callback_data=f"compare_{index}")
        markup.add(button)
    bot.send_message(message.chat.id,
                     "🔍 Оберіть перший товар для порівняння:",
                     reply_markup=markup)


# Обробка вибору товарів для порівняння
@bot.callback_query_handler(func=lambda call: call.data.startswith('compare_'))
def handle_compare(call):
    product_index = int(call.data.split('_')[1])
    chat_id = call.message.chat.id

    if chat_id not in comparison_dict:
        comparison_dict[chat_id] = []

    comparison_dict[chat_id].append(product_index)

    if len(comparison_dict[chat_id]) == 1:
        # Вибір другого товару
        markup = types.InlineKeyboardMarkup()
        for index, product in enumerate(products):
            if index != product_index:
                button = types.InlineKeyboardButton(
                    f"{product['emoji']} {product['name']}",
                    callback_data=f"compare_{index}")
                markup.add(button)
        bot.edit_message_text(
            f"🔍 Порівняння: {products[product_index]['name']} з...",
            chat_id,
            call.message.message_id,
            reply_markup=markup)
    elif len(comparison_dict[chat_id]) == 2:
        # Показуємо порівняння
        show_comparison(call.message, comparison_dict[chat_id])
        comparison_dict[chat_id] = []  # Очищаємо вибір після показу порівняння


def show_comparison(message, product_indices):
    first_product = products[product_indices[0]]
    second_product = products[product_indices[1]]

    comparison = f"🔍 Порівняння:\n\n"
    comparison += f"{first_product['emoji']} {first_product['name']} vs {second_product['emoji']} {second_product['name']}\n\n"

    # Порівнюємо ціни
    comparison += f"💰 Ціна:\n"
    comparison += f"- {first_product['name']}: {first_product['price']}\n"
    comparison += f"- {second_product['name']}: {second_product['price']}\n\n"

    # Порівнюємо знижки
    comparison += f"🏷️ Знижка:\n"
    comparison += f"- {first_product['name']}: {first_product['discount']}\n"
    comparison += f"- {second_product['name']}: {second_product['discount']}\n\n"

    # Порівнюємо рейтинги
    comparison += f"⭐ Рейтинг:\n"
    comparison += f"- {first_product['name']}: {first_product['rating']} ({first_product['reviews']} відгуків)\n"
    comparison += f"- {second_product['name']}: {second_product['rating']} ({second_product['reviews']} відгуків)\n\n"

    # Порівнюємо доставку
    comparison += f"🚚 Доставка:\n"
    comparison += f"- {first_product['name']}: {first_product['delivery']}\n"
    comparison += f"- {second_product['name']}: {second_product['delivery']}\n\n"

    # Порівнюємо характеристики
    comparison += f"📊 Характеристики:\n"
    all_specs = set(first_product['specs'].keys()) | set(
        second_product['specs'].keys())
    for spec in all_specs:
        comparison += f"{spec.capitalize()}:\n"
        comparison += f"- {first_product['name']}: {first_product['specs'].get(spec, 'N/A')}\n"
        comparison += f"- {second_product['name']}: {second_product['specs'].get(spec, 'N/A')}\n\n"

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("🔙 Назад до порівняння",
                                             callback_data="back_to_compare")
    markup.add(back_button)

    bot.edit_message_text(comparison,
                          message.chat.id,
                          message.message_id,
                          reply_markup=markup)


# Обробка кнопки "Назад до порівняння"
@bot.callback_query_handler(func=lambda call: call.data == "back_to_compare")
def back_to_compare(call):
    compare_products(call.message)


# Обробка натискання на кнопку "Підписатися на оновлення"
@bot.message_handler(
    func=lambda message: message.text == '🔔 Підписатися на оновлення')
def subscribe_to_updates(message):
    if message.chat.id not in subscriptions:
        subscriptions[message.chat.id] = set()

    markup = types.InlineKeyboardMarkup()
    options = ['Нові продукти', 'Знижки', 'Відновлення запасів']
    for option in options:
        if option in subscriptions[message.chat.id]:
            button = types.InlineKeyboardButton(
                f"✅ {option}", callback_data=f"unsub_{option}")
        else:
            button = types.InlineKeyboardButton(f"🔔 {option}",
                                                callback_data=f"sub_{option}")
        markup.add(button)

    bot.send_message(message.chat.id,
                     "🔔 Оберіть, на які оновлення ви хочете підписатися:",
                     reply_markup=markup)


# Обробка натискання на кнопку "Знижки та акції"
@bot.message_handler(func=lambda message: message.text == '💸 Знижки та акції')
def show_discounts_and_promotions(message):
    user_id = message.from_user.id
    response = "🎉 Доступні знижки та акції:\n\n"
    
    available_promos = [code for code in promotions if code not in used_promo_codes[user_id]]
    
    if available_promos:
        for code in available_promos:
            promo = promotions[code]
            response += f"🏷️ {promo['name']}\n"
            response += f"   {promo['discount']}% знижки\n"
            response += f"   Код: {code}\n\n"
    else:
        response += "На жаль, у вас зараз немає доступних промокодів. 😔\n"
        response += "Слідкуйте за нашими оновленнями, щоб не пропустити нові акції! 🎁"

    bot.send_message(message.chat.id, response)


# Обробка натискання на кнопку "Мої замовлення"
@bot.message_handler(func=lambda message: message.text == '📦 Мої замовлення')
def show_my_orders(message):
    user_id = message.chat.id
    if user_id not in orders or not orders[user_id]:
        bot.send_message(user_id, "У вас поки немає замовлень. 🛒")
        return

    response = "📦 Ваші замовлення:\n\n"
    for index, order in enumerate(orders[user_id], 1):
        response += f"{index}. {order['emoji']} {order['name']} - {order['price']}\n"

    bot.send_message(user_id, response)


@bot.message_handler(
    func=lambda message: message.text == '📢 Поділитися в соцмережах')
def share_in_social_media(message):
    markup = types.InlineKeyboardMarkup()
    for index, product in enumerate(products):
        button = types.InlineKeyboardButton(
            f"{product['emoji']} {product['name']}",
            callback_data=f"share_product_{index}")
        markup.add(button)
    shop_button = types.InlineKeyboardButton("🏪 Поділитися магазином",
                                             callback_data="share_shop")
    markup.add(shop_button)

    bot.send_message(message.chat.id,
                     "📱 Оберіть товар для поширення або поділіться магазином:",
                     reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('share_product_'))
def share_product(call):
    product_index = int(call.data.split('_')[2])
    product = products[product_index]

    share_text = f"""🚀 Вау! Погляньте на цей неймовірний товар у @TamaShop_Bot! 😍

{product['emoji']} {product['name']}
💰 Ціна: {product['price']}
🏷️ Знижка: {product['discount']}
⭐ Рейтинг: {product['rating']} ({product['reviews']} відгуків)

🛍️ Купуйте в TamaShop - найкрутішому магазині Apple техніки! 🍏✨
Приєднуйтесь до технологічної революції прямо зараз! 🚀🌟"""

    markup = types.InlineKeyboardMarkup()
    telegram_button = types.InlineKeyboardButton(
        "Telegram 📬",
        url=
        f"https://t.me/share/url?url=https://t.me/TamaShopBot&text={share_text}"
    )
    twitter_button = types.InlineKeyboardButton(
        "Twitter 🐦", url=f"https://twitter.com/intent/tweet?text={share_text}")
    facebook_button = types.InlineKeyboardButton(
        "Facebook 👥",
        url=
        f"https://www.facebook.com/sharer/sharer.php?u=https://t.me/TamaShopBot&quote={share_text}"
    )

    markup.add(telegram_button, twitter_button, facebook_button)

    bot.edit_message_text("Оберіть соціальну мережу, щоб поділитися товаром:",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'share_shop')
def share_shop(call):
    share_text = """🎉 Вау! Ви вже чули про TamaShop? 🛍️

🏆 Це найкрутіший магазин Apple техніки, де ви знайдете:
   🍏 Найновіші iPhone, iPad, MacBook
   💼 Неперевершені аксесуари
   🚀 Інноваційні гаджети

💰 Неймовірні ціни та шалені знижки! 🏷️
⚡ Блискавична доставка по всій країні! 🚚
🌟 Бездоганний сервіс та підтримка 24/7! 👨‍💻

Приєднуйтесь до цифрової революції з TamaShop! 🚀✨
👉 https://t.me/TamaShopBot"""

    markup = types.InlineKeyboardMarkup()
    telegram_button = types.InlineKeyboardButton(
        "Telegram 📬",
        url=
        f"https://t.me/share/url?url=https://t.me/TamaShopBot&text={share_text}"
    )
    twitter_button = types.InlineKeyboardButton(
        "Twitter 🐦", url=f"https://twitter.com/intent/tweet?text={share_text}")
    facebook_button = types.InlineKeyboardButton(
        "Facebook 👥",
        url=
        f"https://www.facebook.com/sharer/sharer.php?u=https://t.me/TamaShopBot&quote={share_text}"
    )

    markup.add(telegram_button, twitter_button, facebook_button)

    bot.edit_message_text(
        "Оберіть соціальну мережу, щоб поділитися магазином:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup)


# Обробка підписки/відписки
@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_') or
                            call.data.startswith('unsub_'))
def handle_subscription(call):
    action, option = call.data.split('_')

    # Перевіряємо, чи існує чат у subscriptions, якщо ні, ініціалізуємо його
    if call.message.chat.id not in subscriptions:
        subscriptions[call.message.chat.id] = set()

    if action == 'sub':
        subscriptions[call.message.chat.id].add(option)
        bot.answer_callback_query(call.id,
                                  f"✅ Ви підписались на оновлення: {option}")
    else:
        subscriptions[call.message.chat.id].remove(option)
        bot.answer_callback_query(call.id,
                                  f"❌ Ви відписались від оновлень: {option}")

    # Оновлюємо повідомлення з актуальними підписками
    markup = types.InlineKeyboardMarkup()
    options = ['Нові продукти', 'Знижки', 'Відновлення запасів']
    for opt in options:
        if opt in subscriptions[call.message.chat.id]:
            button = types.InlineKeyboardButton(f"✅ {opt}",
                                                callback_data=f"unsub_{opt}")
        else:
            button = types.InlineKeyboardButton(f"🔔 {opt}",
                                                callback_data=f"sub_{opt}")
        markup.add(button)

    bot.edit_message_reply_markup(call.message.chat.id,
                                   call.message.message_id,
                                   reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🎁 Витратити бали')
def show_available_rewards(message):
    user_id = message.from_user.id
    
    if message.chat.id not in loyalty_points:
        loyalty_points[message.chat.id] = 0

    user_points = loyalty_points[message.chat.id]
    
    # Формуємо відповідь для користувача
    response = f"🎁 Доступні винагороди (у вас {user_points} балів):\n\n"
    
    markup = types.InlineKeyboardMarkup()
    
    # Відображаємо доступні винагороди на основі кількості балів
    for reward_id, reward in rewards.items():
        if user_points >= reward['cost']:
            response += f"✅ {reward['name']} - {reward['cost']} балів\n"
            button = types.InlineKeyboardButton(f"{reward['name']} ({reward['cost']} балів)", callback_data=f"redeem_{reward_id}")
            markup.add(button)
        else:
            response += f"❌ {reward['name']} - {reward['cost']} балів (недостатньо балів)\n"
    
    response += "\nОберіть винагороду, яку хочете отримати:"
    
    # Відправляємо повідомлення користувачу
    bot.send_message(message.chat.id, response, reply_markup=markup)



# Додайте цю функцію для обробки вибору винагороди
@bot.callback_query_handler(func=lambda call: call.data.startswith('redeem_'))
def handle_reward_redemption(call):
    user_id = call.from_user.id
    reward_id = call.data.split('redeem_')[1]
    
    if reward_id in rewards:
        reward = rewards[reward_id]
        if loyalty_points[user_id] >= reward['cost']:
            loyalty_points[user_id] -= reward['cost']
            
            # Логіка для різних типів винагород
            if reward['type'] == 'discount':
                # Додаємо знижку до активних знижок користувача
                active_discounts[user_id] = reward['value']
                response = f"🎉 Ви отримали {reward['value']}% знижку на наступну покупку!"
            elif reward['type'] == 'gift':
                response = f"🎁 Ви отримали подарунок: {reward['name']}! Ми зв'яжемося з вами для уточнення деталей."
            elif reward['type'] == 'service':
                response = f"🛠️ Ви замовили послугу: {reward['name']}. Наш менеджер зв'яжеться з вами для узгодження деталей."
            elif reward['type'] == 'privilege':
                response = f"🌟 Ви отримали привілей: {reward['name']}. Слідкуйте за нашими оновленнями!"
            elif reward['type'] == 'experience':
                response = f"🌈 Ви отримали доступ до: {reward['name']}. Очікуйте подальших інструкцій на вашу електронну пошту."
            elif reward['type'] == 'raffle':
                response = f"🎫 Ви взяли участь у розіграші: {reward['name']}. Результати будуть оголошені незабаром!"
            elif reward['type'] == 'subscription':
                response = f"📱 Ви отримали: {reward['name']}. Код активації буде надіслано вам протягом 24 годин."
            elif reward['type'] == 'membership':
                response = f"🏅 Вітаємо! Ви стали членом: {reward['name']}. Деталі про ваше членство будуть надіслані на вашу електронну пошту."
            else:
                response = f"🎉 Ви успішно обміняли бали на: {reward['name']}!"
            
            response += f"\n\nЗалишок балів: {loyalty_points[user_id]}"
            
            bot.answer_callback_query(call.id, "Винагороду успішно отримано!")
            bot.edit_message_text(response, call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "Недостатньо балів для цієї винагороди!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Помилка: винагороду не знайдено.", show_alert=True)



# Обробка натискання на кнопку "Програма лояльності"
@bot.message_handler(func=lambda message: message.text == '🎁 Програма лояльності')
def show_loyalty_program(message):
    if message.chat.id not in loyalty_points:
        loyalty_points[message.chat.id] = 0

    points = loyalty_points[message.chat.id]
    level = ("Новачок 🥉" if points < 500 else "Учасник 📜" if points < 1000 else "Початківець 💼" if points < 1500 else "Просунутий 🥈" if points < 2500 else "Знавець 🎖️" if points < 4000 else "Експерт 🥇" if points < 6000 else "Професіонал 🔰" if points < 8000 else "Майстер 🌟" if points < 10000 else "Гуру 🧘‍♂️" if points < 15000 else "Легенда 🔱" if points < 20000 else "VIP 👑" if points < 30000 else "Король Apple-техніки 👑🍎" if points < 50000 else "Бог Ґаджетів 🛡️⚔️" if points < 75000 else "Абсолютний Покупець 🚀" if points < 100000 else "Космічний Покупець 🌌")

    response = f"🎁 Ваша програма лояльності:\n\n"
    response += f"🌟 Рівень: {level}\n"
    response += f"💎 Бали: {points}\n\n"
    response += "🎉 Спеціальні пропозиції:\n"
    
    for reward in rewards.values():
        response += f"⭐️ {reward['cost']} балів: {reward['name']}\n"

    markup = types.InlineKeyboardMarkup()
    spend_points_button = types.InlineKeyboardButton("🎁 Витратити бали", callback_data="spend_points")
    markup.add(spend_points_button)

    bot.send_message(message.chat.id, response, reply_markup=markup)

# Додайте цю функцію для обробки натискання кнопки "Витратити бали"
@bot.callback_query_handler(func=lambda call: call.data == "spend_points")
def spend_points_menu(call):
    show_available_rewards(call.message)


# Обробка натискання на кнопку "Відгуки та рейтинги"
@bot.message_handler(
    func=lambda message: message.text == '⭐ Відгуки та рейтинги')
def show_reviews_menu(message):
    markup = types.InlineKeyboardMarkup()
    for index, product in enumerate(products):
        button = types.InlineKeyboardButton(
            f"{product['emoji']} {product['name']}",
            callback_data=f"reviews_{index}")
        markup.add(button)
    bot.send_message(message.chat.id,
                     "⭐ Оберіть товар або магазин для перегляду відгуків:",
                     reply_markup=markup)


# Обробка вибору товару для перегляду відгуків
@bot.callback_query_handler(func=lambda call: call.data.startswith('reviews_'))
def show_product_reviews(call):
    product_index = int(call.data.split('_')[1])
    product = products[product_index]

    if product['name'] not in user_reviews:
        user_reviews[product['name']] = []

    reviews = user_reviews[product['name']]
    response = f"⭐ Відгуки про {product['emoji']} {product['name']}:\n\n"

    if not reviews:
        response += "Поки що немає відгуків. Будьте першим!"
    else:
        for review in reviews:
            response += f"Оцінка: {review['rating']}/5\n"
            response += f"{review['text']}\n"
            response += f"- {review['user']} ({review['date']})\n\n"

    markup = types.InlineKeyboardMarkup()
    add_review_button = types.InlineKeyboardButton(
        "📝 Додати відгук", callback_data=f"add_review_{product_index}")
    back_button = types.InlineKeyboardButton("🔙 Назад",
                                             callback_data="back_to_reviews")
    markup.add(add_review_button, back_button)

    bot.edit_message_text(response,
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


# Обробка додавання відгуку
@bot.callback_query_handler(
    func=lambda call: call.data.startswith('add_review_'))
def add_review(call):
    product_index = int(call.data.split('_')[2])
    product = products[product_index]

    markup = types.InlineKeyboardMarkup()
    for i in range(1, 6):
        markup.add(
            types.InlineKeyboardButton(
                f"Оцінка: {i}", callback_data=f"rate_{product_index}_{i}"))

    bot.edit_message_text(f"Оцініть {product['emoji']} {product['name']}:",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


# Обробка оцінки товару
@bot.callback_query_handler(func=lambda call: call.data.startswith('rate_') and
                            not call.data.startswith('rate_store_'))
def handle_product_rating(call):
    _, product_index, rating = call.data.split('_')
    product_index = int(product_index)
    rating = int(rating)
    product = products[product_index]

    if product['name'] not in product_ratings:
        product_ratings[product['name']] = {'total': 0, 'count': 0}

    product_ratings[product['name']]['total'] += rating
    product_ratings[product['name']]['count'] += 1

    bot.answer_callback_query(call.id, f"Ви оцінили товар на {rating} з 5!")
    bot.send_message(
        call.message.chat.id,
        f"Ви оцінили {product['emoji']} {product['name']} на {rating} з 5.\nТепер, будь ласка, напишіть ваш відгук:"
    )
    bot.register_next_step_handler(call.message, save_product_review,
                                   product['name'], rating)


def save_product_review(message, product_name, rating):
    global user_reviews
    if product_name not in user_reviews:
        user_reviews[product_name] = []

    user_reviews[product_name].append({
        'user':
        message.from_user.first_name,
        'rating':
        rating,
        'text':
        message.text.strip(),
        'date':
        datetime.now().strftime("%Y-%m-%d")
    })

    bot.send_message(message.chat.id,
                     "✅ Дякуємо за ваш відгук! Він допоможе іншим покупцям.")
    show_reviews_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_reviews")
def back_to_reviews(call):
    show_reviews_menu(call.message)


# Обробка натискання на кнопку "Підтримка"
@bot.message_handler(func=lambda message: message.text == '🛠️ Підтримка')
def support(message):
    markup = types.InlineKeyboardMarkup()
    faq_button = types.InlineKeyboardButton("❓ Часті запитання",
                                            callback_data="faq")
    contact_button = types.InlineKeyboardButton(
        "👤 Зв'язатися з підтримкою", callback_data="contact_support")
    markup.add(faq_button, contact_button)
    bot.send_message(message.chat.id,
                     "🛠️ Чим ми можемо вам допомогти?",
                     reply_markup=markup)


# Обробка вибору "Наші переваги"
@bot.callback_query_handler(func=lambda call: call.data == "faq")
def show_faq(call):
    markup = types.InlineKeyboardMarkup()
    questions = [
        "Переваги", "Оплата",
        "Доставка"
    ]
    for i, question in enumerate(questions, 1):
        markup.add(
            types.InlineKeyboardButton(f"{i}. {question}",
                                       callback_data=f"faq_{i}"))
    bot.edit_message_text("❓ Оберіть питання, яке вас цікавить:",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


# Обробка вибору конкретного питання FAQ
@bot.callback_query_handler(func=lambda call: call.data.startswith("faq_"))
def answer_faq(call):
    question_id = int(call.data.split("_")[1])
    answers = {
        1:
       "📱 **Наші переваги**\n\nМи пропонуємо оригінальну техніку Apple з професійним налаштуванням та індивідуальним підходом. Кожен пристрій проходить ретельну перевірку нашими досвідченими фахівцями, щоб гарантувати його бездоганну роботу на найвищому рівні. Також ми беремо на себе перше налаштування вашої техніки, допомагаючи вам швидко почати користуватися всіма можливостями вашого пристрою Apple.\n\n**Особлива послуга** — розширена гарантія лише за 500 грн на рік. Вона включає налаштування всіх необхідних додатків, оптимізацію роботи пристрою та вирішення проблем з прошивкою.",
        2:
        "💳 **Оплата**\n\nПроцес оплати максимально зручний та гнучкий. Ви можете оплатити банківською карткою або криптовалютою. Також доступна оплата при отриманні: на касі поштового відділення чи в нашому магазині.",
        3:
        "🚚 **Доставка**\n\nМи пропонуємо безкоштовну доставку по всій Україні та за кордон. Термін доставки по Україні — від 3 до 7 днів, а для замовлень з-за кордону — 7-14 днів. Співпрацюємо з Meest, Nova Пошта та Укрпошта для швидкого та безпечного отримання вашого замовлення.",
    }
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("🔙 Назад до FAQ",
                                             callback_data="faq")
    contact_button = types.InlineKeyboardButton(
        "👤 Зв'язатися з підтримкою", callback_data="contact_support")
    markup.add(back_button, contact_button)
    bot.edit_message_text(f"❓ {answers[question_id]}",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


# Обробка запиту на зв'язок з підтримкою
@bot.callback_query_handler(func=lambda call: call.data == "contact_support")
def contact_support(call):
    markup = types.InlineKeyboardMarkup()
    chat_button = types.InlineKeyboardButton("💬 Чат з оператором",
                                             callback_data="chat_support")
    email_button = types.InlineKeyboardButton("📧 Написати повідмолення",
                                              callback_data="email_support")
    markup.add(chat_button, email_button)
    bot.edit_message_text("👤 Виберіть спосіб зв'язку з підтримкою:",
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=markup)


# Обробка запиту на чат з оператором
@bot.callback_query_handler(func=lambda call: call.data == "chat_support")
def chat_with_support(call):
    # Тут можна додати логіку для з'єднання з живим оператором
    bot.answer_callback_query(
        call.id, "👨‍💼 Зачекайте, будь ласка. Ми з'єднуємо вас з оператором...")
    bot.send_message(
        call.message.chat.id,
        "😂👌 Всі наші оператори зайняті на всі 100%! Ви можете звернутися знову — ніколи 😜! Дякуємо за ваше терпіння! 🙏✨")


# Обробка запиту на відправку email
@bot.callback_query_handler(func=lambda call: call.data == "email_support")
def email_support(call):
    bot.send_message(
        call.message.chat.id,
        "📧 Будь ласка, напишіть ваше питання або проблему. Ми відправимо це на адресу нашої підтримки."
    )
    bot.register_next_step_handler(call.message, process_email_support)


def process_email_support(message):
    bot.send_message(
        message.chat.id,
        f"😴 Вибачте, але ваше повідомлення не буде відправлено, оскільки наш бот трохи втомився! 🥱☕ Дякуємо за розуміння і гарного дня! 😅"
    )


# Функція для відправки повідомлень підтримки (використовується адміністратором)
def send_support_message(user_id, message):
    try:
        bot.send_message(user_id, f"👨‍💼 Повідомлення від підтримки: {message}")
        return True
    except telebot.apihelper.ApiException as e:
        if e.result.status_code == 400 and "chat not found" in str(e):
            print(f"Користувач {user_id} не знайдений або заблокував бота.")
        else:
            print(f"Помилка при відправці повідомлення підтримки: {e}")
        return False
    except Exception as e:
        print(f"Неочікувана помилка при відправці повідомлення підтримки: {e}")
        return False

# Команда для адміністратора, щоб додати бали лояльності користувачу
@bot.message_handler(commands=['add_points'])
def admin_add_points(message):
    if message.from_user.id != support_user_id:
        bot.reply_to(message, "❌ У вас немає прав для використання цієї команди.")
        return

    try:
        _, user_id, points = message.text.split()
        user_id = int(user_id)
        points = int(points)
        
        if user_id not in loyalty_points:
            loyalty_points[user_id] = 0
        
        loyalty_points[user_id] += points
        
        bot.reply_to(message, f"✅ Користувачу {user_id} успішно додано {points} балів лояльності. Загальна кількість балів: {loyalty_points[user_id]}")
        
        # Спробуємо відправити повідомлення користувачу про нараховані бали
        try:
            bot.send_message(user_id, f"🎉 Вітаємо! Вам було нараховано {points} балів лояльності. Ваш загальний баланс: {loyalty_points[user_id]} балів.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Бали нараховано, але не вдалося відправити повідомлення користувачу. Помилка: {str(e)}")
        
    except ValueError:
        bot.reply_to(message, "❌ Некоректний формат команди. Використовуйте: /add_points [user_id] [кількість_балів]")
    except Exception as e:
        bot.reply_to(message, f"❌ Виникла помилка при додаванні балів: {str(e)}")
        
# Команда для адміністратора, щоб відняти бали лояльності користувачу
@bot.message_handler(commands=['remove_points'])
def admin_add_points(message):
    if message.from_user.id != support_user_id:
        bot.reply_to(message, "❌ У вас немає прав для використання цієї команди.")
        return

    try:
        _, user_id, points = message.text.split()
        user_id = int(user_id)
        points = int(points)
        
        if user_id not in loyalty_points:
            loyalty_points[user_id] = 0
        
        loyalty_points[user_id] -= points
        
        bot.reply_to(message, f"✅ Користувачу {user_id} успішно видалено {points} балів лояльності. Загальна кількість балів: {loyalty_points[user_id]}")
        
        # Спробуємо відправити повідомлення користувачу про нараховані бали
        try:
            bot.send_message(user_id, f"🎉 Співчуваємо! У Вас було видалено {points} балів лояльності. Ваш загальний баланс: {loyalty_points[user_id]} балів.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Бали видалено, але не вдалося відправити повідомлення користувачу. Помилка: {str(e)}")
        
    except ValueError:
        bot.reply_to(message, "❌ Некоректний формат команди. Використовуйте: /remove_points [user_id] [кількість_балів]")
    except Exception as e:
        bot.reply_to(message, f"❌ Виникла помилка при додаванні балів: {str(e)}")

# Команда для адміністратора, щоб відповісти користувачу
@bot.message_handler(commands=['reply'])
def admin_reply(message):
    if message.from_user.id != support_user_id:
        bot.reply_to(message,
                     "❌ У вас немає прав для використання цієї команди.")
        return

    try:
        _, user_id, *text = message.text.split()
        user_id = int(user_id)
        reply_text = " ".join(text)
        if send_support_message(user_id, reply_text):
            bot.reply_to(
                message,
                f"✅ Повідомлення успішно відправлено користувачу {user_id}")
        else:
            bot.reply_to(
                message,
                f"❌ Не вдалося відправити повідомлення користувачу {user_id}")
    except ValueError:
        bot.reply_to(
            message,
            "❌ Некоректний формат команди. Використовуйте: /reply [user_id] [текст відповіді]"
        )

# Пример обработчика команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Bot is active.")
    
    
    
# Запуск бота в режиме polling
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("Bot stopped manually.")
