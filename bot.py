import telebot
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "").lstrip("@")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]
ZEUS_SOURCE_URL = os.getenv(
    "ZEUS_SOURCE_URL",
    "https://raw.githubusercontent.com/panel-zeus/Z-E-U-S/main/Source.js"
)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")

bot = telebot.TeleBot(BOT_TOKEN)

# ==================== دکمه‌های خیلی قوی ====================
def sponsor_kb():
    return telebot.types.InlineKeyboardMarkup(inline_keyboard=[
        [telebot.types.InlineKeyboardButton("📥 ربات دانلودر اینستاگرام رایگان", url="https://t.me/FaraDownloaderBot")],
        [telebot.types.InlineKeyboardButton("🔐 آموزش و فروش V2ray_company | VPN", url="https://t.me/V2ray_company")],
        [telebot.types.InlineKeyboardButton("✅ عضویت در کانال (اجباری)", url=f"https://t.me/{REQUIRED_CHANNEL}" if REQUIRED_CHANNEL else "https://t.me/")],
        [telebot.types.InlineKeyboardButton("🔄 بررسی عضویت و ورود به ربات", callback_data="check_join")]
    ])

def main_menu_kb():
    return telebot.types.InlineKeyboardMarkup(inline_keyboard=[
        [telebot.types.InlineKeyboardButton("🚀 ساخت پنل جدید", callback_data="new_panel")],
        [telebot.types.InlineKeyboardButton("⚙️ مدیریت و آپدیت پنل‌ها", callback_data="manage_panels")],
        [telebot.types.InlineKeyboardButton("➕ ثبت اکانت کلودفلر", callback_data="add_cf_account")]
    ])

def cf_token_kb():
    token_url = "https://dash.cloudflare.com/profile/api-tokens?permissionGroupKeys=%5B%7B%22key%22%3A%22workers_scripts%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22workers_kv_storage%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22d1%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22account_settings%22%2C%22type%22%3A%22read%22%7D%2C%7B%22key%22%3A%22workers_subdomain%22%2C%22type%22%3A%22edit%22%7D%2C%7B%22key%22%3A%22account_analytics%22%2C%22type%22%3A%22read%22%7D%2C%7B%22key%22%3A%22user_details%22%2C%22type%22%3A%22read%22%7D%5D&accountId=*&zoneId=all&name=Zeus-Deployer-Token"
    return telebot.types.InlineKeyboardMarkup(inline_keyboard=[
        [telebot.types.InlineKeyboardButton("🔐 ورود به حساب کلودفلر", url="https://dash.cloudflare.com/login")],
        [telebot.types.InlineKeyboardButton("🎫 دریافت توکن کلودفلر برای زئوس", url=token_url)],
        [telebot.types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
    ])

# ==================== چک عضویت اجباری ====================
def check_channel_membership(user_id):
    if not REQUIRED_CHANNEL:
        return True
    try:
        member = bot.get_chat_member(f"@{REQUIRED_CHANNEL}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ==================== شروع ربات ====================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if REQUIRED_CHANNEL and not check_channel_membership(user_id):
        text = "⚠️ <b>عضویت اجباری در کانال</b>\n\nبرای استفاده از ربات حتماً باید در کانال زیر عضو شوید.\nبعد از عضویت روی دکمه «بررسی عضویت» بزنید."
        bot.reply_to(message, text, reply_markup=sponsor_kb(), parse_mode="HTML")
        return

    bot.reply_to(message, "🚀 <b>ایزی پنل ماکر - پنل زئوس</b>\n\nربات اختصاصی ساخت پنل کانفینگ زئوس\n\nاز منوی زیر گزینه مورد نظر را انتخاب کنید:", reply_markup=main_menu_kb(), parse_mode="HTML")

# ==================== دکمه‌های اصلی ====================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "check_join":
        if check_channel_membership(call.from_user.id):
            bot.answer_callback_query(call.id)
            bot.edit_message_text("✅ عضویت شما تایید شد!\n\nسلام <b>{}</b>\nاز منوی زیر گزینه مورد نظر را انتخاب کنید:".format(call.from_user.first_name),
                                call.message.chat.id, call.message.message_id,
                                reply_markup=main_menu_kb(), parse_mode="HTML")
        else:
            bot.answer_callback_query(call.id, "❌ هنوز در کانال عضو نشده‌اید!", show_alert=True)

    elif call.data == "back_main":
        bot.edit_message_text("منوی اصلی:\nاز گزینه‌های زیر انتخاب کنید:", call.message.chat.id, call.message.message_id, reply_markup=main_menu_kb())

    elif call.data == "add_cf_account":
        text = "☁️ <b>اتصال اکانت جدید کلودفلر به زئوس</b> ☁️\n\n⚠️ توجه بسیار مهم:\nلطفاً مراحل زیر را به ترتیب انجام دهید."
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cf_token_kb(), parse_mode="HTML")

    elif call.data == "new_panel":
        # اینجا می‌تونیم لیست اکانت‌ها رو اضافه کنیم ولی فعلاً ساده نگه داریم
        bot.edit_message_text("🚀 <b>تایید استقرار پنل</b>\nبرای ساخت پنل جدید روی اکانت زیر کلیک کنید:", call.message.chat.id, call.message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("در حال توسعه...", callback_data="coming")))

    elif call.data == "manage_panels":
        bot.edit_message_text("⚙️ <b>مدیریت و آپدیت پنل‌ها</b>\nدر حال توسعه...", call.message.chat.id, call.message.message_id)

# ==================== دریافت توکن ====================
@bot.message_handler(content_types=['text'])
def handle_token(message):
    token = message.text.strip()
    # اینجا می‌تونیم توکن رو چک کنیم و پنل بسازیم
    bot.reply_to(message, "✅ توکن دریافت شد! پنل در حال ساخت و آپدیت در Cloudflare...")

bot.polling(none_stop=True, interval=0, timeout=30)
