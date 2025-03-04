import requests
from datetime import datetime
import jdatetime
from balethon import Client, Message, Keyboard, InlineKeyboard

# تنظیمات ربات
BOT_TOKEN = "1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
bot = Client(BOT_TOKEN)

# ----------------- توابع پردازش داده -----------------

# دریافت زمان و تاریخ
def get_time():
    now = datetime.now()
    jalali_date = jdatetime.date.fromgregorian(date=now)
    return (f"⏳ **زمان فعلی:**\n"
            f"📅 **تاریخ شمسی:** {jalali_date.strftime('%Y/%m/%d')}\n"
            f"📆 **تاریخ میلادی:** {now.strftime('%Y-%m-%d')}\n"
            f"⏰ **ساعت:** {now.strftime('%H:%M:%S')}\n"
            f"📖 **روز:** {jalali_date.strftime('%A')}\n"
            f"🗓 **ماه:** {jalali_date.strftime('%B')} - {jalali_date.year}")

# دریافت حدیث تصادفی از API صحیح
def get_hadith():
    url = "https://din-esi.onrender.com/random_hadith"
    response = requests.get(url).json()
    if "hadith" in response and "speaker" in response:
        return f"📜 **حدیث امروز:**\n\n❝ {response['hadith']} ❞\n\n🗣 **راوی:** {response['speaker']}"
    return "⚠ خطا در دریافت حدیث!"

# چت با هوش مصنوعی اسلامی
def chat_with_ai(message):
    url = f"https://open.wiki-api.ir/apis-1/ChatGPT-4o?q={message}"
    response = requests.get(url).json()
    return response.get("results", "🤖 هوش مصنوعی پاسخی نداشت.") if response.get("status") else "⚠ خطا در ارتباط با هوش مصنوعی!"

# پیگیری مرسوله تیپاکس
def track_parcel(tracking_code):
    url = f"https://open.wiki-api.ir/apis-1/TipaxInfo?code={tracking_code}"
    response = requests.get(url).json()
    if not response.get("status"):
        return "⚠ کد رهگیری نامعتبر است یا اطلاعاتی یافت نشد."
    
    results = response["results"]
    sender, receiver, status_info = results["sender"], results["receiver"], results["status_info"]
    
    return (f"📦 **وضعیت مرسوله:**\n"
            f"📌 **فرستنده:** {sender['name']} - {sender['city']}\n"
            f"📍 **گیرنده:** {receiver['name']} - {receiver['city']}\n"
            f"📆 **تاریخ ثبت سفارش:** {status_info[0]['date']}\n"
            f"🚛 **آخرین وضعیت:** {status_info[0]['status']}")

# ترجمه متن به فارسی
def translate_to_farsi(text):
    url = f"https://open.wiki-api.ir/apis-1/GoogleTranslate?text={text}&to=fa"
    response = requests.get(url).json()
    return response.get("results", "⚠ ترجمه‌ای پیدا نشد.") if response.get("status") else "⚠ خطا در ترجمه!"

# ----------------- هندلرهای ربات -----------------

# دکمه‌های منوی اصلی
def get_main_menu():
    return Keyboard([
        ["📅 اعلام زمان"],
        ["📖 حدیث تصادفی"],
        ["🤖 چت با هوش مصنوعی"],
        ["📦 پیگیری مرسوله تیپاکس"],
        ["🌍 ترجمه به فارسی"]
    ], resize_keyboard=True)

# دکمه‌های بازگشت
def get_back_button():
    return Keyboard([["🔙 بازگشت به منو اصلی"]], resize_keyboard=True)

@bot.on_message()
async def handle_message(client: Client, message: Message):
    text = message.text

    if text == "/start" or text == "🔙 بازگشت به منو اصلی":
        await message.reply("👋 سلام! به ربات **صراط** خوش آمدید.\nیک گزینه را انتخاب کنید:", 
                            reply_markup=get_main_menu())

    elif text == "📅 اعلام زمان":
        await message.reply(get_time(), reply_markup=get_back_button())

    elif text == "📖 حدیث تصادفی":
        await message.reply(get_hadith(), reply_markup=get_back_button())

    elif text == "🤖 چت با هوش مصنوعی":
        await message.reply("🗨 لطفاً سوال خود را ارسال کنید:", reply_markup=get_back_button())
        bot.state.set(message.chat.id, "ai_chat")

    elif text == "📦 پیگیری مرسوله تیپاکس":
        await message.reply("📦 لطفاً کد رهگیری مرسوله را ارسال کنید:", reply_markup=get_back_button())
        bot.state.set(message.chat.id, "track_parcel")

    elif text == "🌍 ترجمه به فارسی":
        await message.reply("🌍 لطفاً متن مورد نظر برای ترجمه را ارسال کنید:", reply_markup=get_back_button())
        bot.state.set(message.chat.id, "translate")

    else:
        state = bot.state.get(message.chat.id)
        if state == "ai_chat":
            await message.reply(chat_with_ai(text), reply_markup=get_back_button())
        elif state == "track_parcel":
            await message.reply(track_parcel(text), reply_markup=get_back_button())
        elif state == "translate":
            await message.reply(translate_to_farsi(text), reply_markup=get_back_button())
        else:
            await message.reply("⚠ دستور نامعتبر! لطفاً از دکمه‌ها استفاده کنید.", reply_markup=get_main_menu())

# ----------------- اجرای ربات -----------------
bot.run()
