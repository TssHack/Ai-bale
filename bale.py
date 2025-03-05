from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard
import requests
from datetime import datetime
import jdatetime
import pytz

# تنظیمات ربات
bot_token = "‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
bot = Client(bot_token)

# وضعیت کاربران
user_states = {}

# تابع دریافت تاریخ و زمان
def get_time():
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.now(iran_tz)
    jalali_date = jdatetime.date.fromgregorian(date=now)
    return f"""🕰️ اعلام زمان:

📆 تاریخ شمسی: {jalali_date.strftime("%Y/%m/%d")}
🌍 تاریخ میلادی: {now.strftime("%Y-%m-%d")}
🌙 تاریخ قمری: {now.strftime("%d/%m/%Y")}

⏰ ساعت: {now.strftime("%H:%M:%S")}
📅 روز هفته: {jalali_date.strftime("%A")}
🗓️ ماه: {jalali_date.strftime("%B")}
🗓️ سال: {jalali_date.year}
"""

# دریافت حدیث
def get_hadith():
    try:
        response = requests.get("https://din-esi.onrender.com/random_hadith")
        data = response.json()
        return f"📖 {data.get('hadith', 'حدیثی پیدا نشد.')}\n🗣️ {data.get('speaker', 'نامشخص')}"
    except:
        return "مشکلی در دریافت حدیث رخ داد."

# چت هوش مصنوعی
def chat_with_ai(text):
    try:
        response = requests.get(f"https://momen-api.onrender.com/?text={text}")
        data = response.json()
        return data.get("message", "پاسخی دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور."

# ترجمه متن
def translate_to_farsi(text):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/GoogleTranslate?text={text}&to=fa")
        data = response.json()
        return data.get("results", "ترجمه‌ای پیدا نشد.")
    except:
        return "مشکلی در ترجمه رخ داد."

# پیگیری مرسوله تیپاکس
def track_parcel(tracking_code):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/TipaxInfo?code={tracking_code}")
        data = response.json()
        if data["status"]:
            results = data["results"]
            sender = results["sender"]
            receiver = results["receiver"]
            status_info = results["status_info"]
            return f"""📦 پیگیری مرسوله:

📤 فرستنده: {sender['name']} از {sender['city']}
📥 گیرنده: {receiver['name']} در {receiver['city']}
💳 هزینه: {results['total_cost']} تومان
🛳 وزن: {results['weight']} کیلوگرم

🚦 وضعیت‌ها:
{', '.join([f"{status['date']} - {status['status']}" for status in status_info])}"""
        return "کد رهگیری نامعتبر است."
    except:
        return "مشکلی در دریافت اطلاعات مرسوله رخ داد."

# دریافت جوک
def get_joke():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/4Jok?page=500")
        data = response.json()
        return f"😂 {data['results']['post']}"
    except:
        return "مشکلی در دریافت جوک رخ داد."

# دریافت نرخ طلا و سکه
def get_gold_rate():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/GoldRate")
        data = response.json()
        prices = data["results"]["prices"]
        text = "💰 نرخ طلا و سکه:\n\n"
        for item in prices:
            change = "🔺" if item["is_positive"] else "🔻"
            text += f"{item['name']}: {item['price']} ریال ({change} {item['change_value']})\n"
        return text
    except:
        return "مشکلی در دریافت نرخ طلا و سکه رخ داد."

# دکمه‌ها
inline_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("حدیث گو 📖", "hadith")],
    [("جوک بگو 😂", "joke"), ("نرخ طلا و سکه 💰", "gold_rate")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("دستیار مومن 🤖", "ai_chat"), ("ترجمه به فارسی 📝", "translate")],
    [("اطلاعات سازنده 🧑‍💻", "info")]
)

reply_keyboard = ReplyKeyboard(["منوی اصلی 🏠"])

# پیام‌های دریافتی
@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if state == "tracking":
        await message.reply(track_parcel(message.text), reply_markup=inline_buttons)
    elif state == "translate":
        await message.reply(translate_to_farsi(message.text), reply_markup=inline_buttons)
    elif state == "ai_chat":
        await message.reply(chat_with_ai(message.text), reply_markup=inline_buttons)
    else:
        await message.reply("سلام! لطفاً گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_buttons)
    
    if state not in ["ai_chat"]:
        user_states[chat_id] = None

# دکمه‌های اینلاین
@bot.on_callback_query()
async def on_callback(callback_query):
    chat_id = callback_query.message.chat.id

    if callback_query.data == "time":
        await callback_query.message.edit_text(get_time(), reply_markup=inline_buttons)

    elif callback_query.data == "hadith":
        await callback_query.message.edit_text(get_hadith(), reply_markup=inline_buttons)

    elif callback_query.data == "joke":
        await callback_query.message.edit_text(get_joke(), reply_markup=inline_buttons)

    elif callback_query.data == "gold_rate":
        await callback_query.message.edit_text(get_gold_rate(), reply_markup=inline_buttons)

    elif callback_query.data == "track_parcel":
        user_states[chat_id] = "tracking"
        await callback_query.message.edit_text("لطفاً کد رهگیری خود را ارسال کنید.")

    elif callback_query.data == "translate":
        user_states[chat_id] = "translate"
        await callback_query.message.edit_text("لطفاً متن مورد نظر خود را ارسال کنید.")

    elif callback_query.data == "ai_chat":
        user_states[chat_id] = "ai_chat"
        await callback_query.message.edit_text("پیام خود را ارسال کنید.")

    elif callback_query.data == "info":
        await callback_query.message.edit_text("این ربات توسط تیم شفق ساخته شده است.\nارتباط: @Devehsan", reply_markup=inline_buttons)

# اجرای ربات
bot.run()
