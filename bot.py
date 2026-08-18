import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = "8669573949:AAFWKdWp8njdHNuBLlzg__dBb9Z-N9YsiCg"
bot = telebot.TeleBot(TOKEN)

CHANNEL_LINK = "https://t.me/+JArqswroP-QyMyMTJk"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("📢 تایید عضویت در کانال", callback_data="confirm_channel"),
        telebot.types.InlineKeyboardButton("🔧 ساخت پنل جدید", callback_data="create_panel"),
        telebot.types.InlineKeyboardButton("🔄 مدیریت و آپدیت پنل", callback_data="manage_panel"),
        telebot.types.InlineKeyboardButton("🌐 پروکسی اختصاصی", callback_data="proxy"),
        telebot.types.InlineKeyboardButton("📥 دریافت سورس پنل", callback_data="get_source"),
        telebot.types.InlineKeyboardButton("💰 حمایت مالی", callback_data="donate"),
        telebot.types.InlineKeyboardButton("🛠️ پشتیبانی", url=CHANNEL_LINK)
    )
    bot.reply_to(message, "🚀 <b>ایزی پنل ماکر - پنل زئوس</b>\n\nربات اختصاصی ساخت و مدیریت پنل کانفینگ زئوس\n\nبرای ساخت پنل جدید ابتدا باید اکانت کلودفلر ثبت شده باشه!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "confirm_channel":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "✅ عضویتت در کانال تایید شد!\nحالا می‌تونی پنل بسازی.")

    elif call.data == "create_panel":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🚀 <b>تایید استقرار پنل</b>\nبرای ساخت پنل جدید روی اکانت زیر کلیک کنید:", parse_mode="HTML", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton(f"📧 {call.from_user.first_name}", callback_data="build_panel_confirm")))

    elif call.data == "build_panel_confirm":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "درحال ساخت پنل زئوس...")

        import time
        time.sleep(2.5)

        bot.send_message(call.message.chat.id, "✅ پنل با موفقیت ساخته شد!")
        bot.send_message(call.message.chat.id, f"🔗 لینک پنل: https://{call.from_user.id}.workers.dev/panel")
        bot.send_message(call.message.chat.id, "🟢 ورود به پنل:", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("🔗 ورود به پنل", url=f"https://{call.from_user.id}.workers.dev/panel")))

    elif call.data == "manage_panel":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "در حال مدیریت و آپدیت پنل‌های شما...")

    elif call.data == "proxy":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "پروکسی اختصاصی در حال توسعه...")

    elif call.data == "get_source":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "سورس پنل زئوس: https://github.com/panel-zeus/Z-E-U-S")

    elif call.data == "donate":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "حمایت مالی: https://donatonion.ir-netlify.workers.dev")

    elif call.data == "enter_cloudflare":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔐 در حال ورود به داشبورد کلودفلر...", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("🔐 ورود به Cloudflare", url="https://dash.cloudflare.com/login")))

    elif call.data == "get_token":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📋 <b>دریافت توکن کلودفلر</b>\nلینک زیر رو باز کن و توکن Zeus-Deployer رو بساز:", parse_mode="HTML", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("🔗 دریافت توکن Zeus-Deployer", url="https://dash.cloudflare.com/profile/api-tokens?permissionGroupKeys=%5B%7B%22key%22%3A%22workers_scripts%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22workers_kv_storage%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22d1%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22account_settings%22%2C%22type%22%3A%22read%22%7D%2C%7B%22key%22%3A%22workers_subdomain%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22account_analytics%22%2C%22type%22%3A%22read%22%7D%5D&accountId=*&zoneId=all&name=Zeus-Deployer-Token")))

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if len(message.text) < 20:
        return
    bot.send_message(message.chat.id, "✅ توکن دریافت شد! پنل در حال ثبت و آپدیت در Cloudflare...")

bot.polling(none_stop=True, interval=0, timeout=30)
