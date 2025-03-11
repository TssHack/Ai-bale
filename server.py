import json
import os
from balethon import Client

# توکن ربات را اینجا وارد کنید
BOT_TOKEN = "توکن_ربات_بله"

# مسیر فایل JSON برای ذخیره کاربران
USER_DATA_FILE = "users.json"

# ایجاد کلاینت ربات
bot = Client(BOT_TOKEN)

# تابع برای خواندن اطلاعات کاربران از فایل
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return []

# تابع برای ذخیره اطلاعات کاربران در فایل
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# لیست کاربران را بارگذاری می‌کنیم
users = load_users()

@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id  # دریافت شناسه عددی کاربر
    text = message.text.strip()  # دریافت متن پیام

    if text == "/listuser":  # اگر دستور لیست کاربران ارسال شد
        if users:
            users_list = "\n".join(str(user) for user in users)
            await message.reply(f"📜 لیست کاربران ثبت‌شده:\n\n{users_list}")
        else:
            await message.reply("⛔ هنوز هیچ کاربری ثبت نشده است.")

    elif chat_id not in users:  # ثبت خودکار کاربر بدون ارسال پیام
        users.append(chat_id)
        save_users(users)

# اجرای ربات
bot.run()
