from balethon import Client
from balethon.conditions import private
from balethon.objects import InlineKeyboard
import requests

bot = Client("‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO")

# تابع دریافت زمان و تاریخ
def get_time():
    from datetime import datetime
    import jdatetime
    now = datetime.now()
    jalali_date = jdatetime.date.fromgregorian(date=now)
    time_info = {
        "shamsi_date": jalali_date.strftime("%Y/%m/%d"),
        "gregorian_date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": jalali_date.strftime("%A"),
        "month": jalali_date.strftime("%B"),
        "year": jalali_date.year
    }
    return time_info

# تابع دریافت حدیث از API
def get_hadith():
    url = "https://din-esi.onrender.com/random_hadith"
    response = requests.get(url)
    data = response.json()
    return f"حدیث امروز: {data.get('hadith')} \nگفته: {data.get('speaker')}"

# تابع چت با هوش مصنوعی
def chat_with_ai(user_message):
    url = f"https://open.wiki-api.ir/apis-1/ChatGPT-4o?q={user_message}"
    response = requests.get(url)
    data = response.json()
    return data.get("results", "پاسخی از هوش مصنوعی دریافت نشد.")

# تابع پیگیری مرسوله تیپاکس
def track_parcel(tracking_code):
    url = f"https://open.wiki-api.ir/apis-1/TipaxInfo?code={tracking_code}"
    response = requests.get(url)
    data = response.json()
    if data["status"]:
        results = data["results"]
        sender = results["sender"]
        receiver = results["receiver"]
        status_info = results["status_info"]
        parcel_info = f"📤 فرستنده: {sender['name']} از {sender['city']}\n"
        parcel_info += f"📥 گیرنده: {receiver['name']} در {receiver['city']}\n"
        parcel_info += f"📅 تاریخ ثبت سفارش: {status_info[0]['date']} - وضعیت: {status_info[0]['status']}"
        return parcel_info
    return "❌ اطلاعات مرسوله پیدا نشد."

# تابع ترجمه به فارسی
def translate_to_farsi(text):
    url = f"https://open.wiki-api.ir/apis-1/GoogleTranslate?text={text}&to=fa"
    response = requests.get(url)
    data = response.json()
    return data.get("results", "ترجمه‌ای پیدا نشد.")

# دکمه‌های ربات
@bot.on_message(private)
async def answer_message(message):
    buttons = [
        ("🕰 نمایش زمان", "time"),
        ("📜 حدیث امروز", "hadith"),
        ("🤖 چت با هوش مصنوعی", "ai_chat"),
        ("📦 پیگیری مرسوله تیپاکس", "track_parcel"),
        ("🌍 ترجمه به فارسی", "translate")
    ]
    inline_buttons = InlineKeyboard(
        *[[(label, data)] for label, data in buttons]
    )
    await message.reply(
        "سلام! به ربات صراط خوش آمدید.\nلطفاً گزینه مورد نظر خود را انتخاب کنید:",
        inline_keyboard=inline_buttons
    )

# دکمه‌ها برای پاسخ دادن
@bot.on_callback_query()
async def on_callback_query(callback_query):
    if callback_query.data == "time":
        time_info = get_time()
        await callback_query.answer(
            f"زمان به وقت ایران:\n\n"
            f"📅 تاریخ شمسی: {time_info['shamsi_date']}\n"
            f"📅 تاریخ میلادی: {time_info['gregorian_date']}\n"
            f"🕒 زمان: {time_info['time']}\n"
            f"🌞 روز: {time_info['day']}\n"
            f"📅 ماه: {time_info['month']}\n"
            f"📆 سال: {time_info['year']}"
        )
    elif callback_query.data == "hadith":
        hadith = get_hadith()
        await callback_query.answer(hadith)
    elif callback_query.data == "ai_chat":
        await callback_query.answer("برای شروع چت با هوش مصنوعی پیامی ارسال کنید.")
        @bot.on_message(private)
        async def on_message_ai(message):
            ai_response = chat_with_ai(message.text)
            await message.reply(ai_response)
    elif callback_query.data == "track_parcel":
        await callback_query.answer("لطفاً کد رهگیری مرسوله را وارد کنید:")
        @bot.on_message(private)
        async def on_message_tracking(message):
            parcel_info = track_parcel(message.text)
            await message.reply(parcel_info)
    elif callback_query.data == "translate":
        await callback_query.answer("لطفاً متنی که می‌خواهید ترجمه شود را ارسال کنید:")
        @bot.on_message(private)
        async def on_message_translation(message):
            translation = translate_to_farsi(message.text)
            await message.reply(translation)

bot.run()
