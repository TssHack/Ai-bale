import requests
from datetime import datetime
import jdatetime
from balepy import Client, types

# تنظیمات ربات
BOT_TOKEN = "‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
app = Client("sirat_bot", bot_token=BOT_TOKEN)

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
    return types.ReplyMarkup([
        [types.Button.text("📅 اعلام زمان", data="time")],
        [types.Button.text("📖 حدیث تصادفی", data="hadith")],
        [types.Button.text("🤖 چت با هوش مصنوعی", data="ai_chat")],
        [types.Button.text("📦 پیگیری مرسوله تیپاکس", data="track_parcel")],
        [types.Button.text("🌍 ترجمه به فارسی", data="translate")]
    ])

# دکمه‌های بازگشت
def get_back_button():
    return types.ReplyMarkup([[types.Button.text("🔙 بازگشت به منو اصلی", data="back_to_menu")]])

@app.on_message(types.MessageCommand("start"))
async def on_start(ctx: types.Message):
    await ctx.answer("👋 سلام! به ربات **صراط** خوش آمدید.\nیک گزینه را انتخاب کنید:", 
                     reply_markup=get_main_menu())

# مدیریت دکمه‌ها
@app.on_callback_query()
async def on_callback(ctx: types.CallbackQuery):
    if ctx.data == "time":
        await ctx.answer(get_time(), reply_markup=get_back_button())

    elif ctx.data == "hadith":
        await ctx.answer(get_hadith(), reply_markup=get_back_button())

    elif ctx.data == "ai_chat":
        await ctx.answer("🗨 لطفاً سوال خود را ارسال کنید.", reply_markup=types.ReplyMarkup(force_reply=True))

    elif ctx.data == "track_parcel":
        await ctx.answer("📦 لطفاً کد رهگیری مرسوله را ارسال کنید.", reply_markup=types.ReplyMarkup(force_reply=True))

    elif ctx.data == "translate":
        await ctx.answer("🌍 لطفاً متن مورد نظر برای ترجمه را ارسال کنید.", reply_markup=types.ReplyMarkup(force_reply=True))

    elif ctx.data == "back_to_menu":
        await ctx.answer("🔙 برگشت به منو اصلی", reply_markup=get_main_menu())

# مدیریت ورودی‌های کاربر
@app.on_message(types.Message)
async def handle_user_message(ctx: types.Message):
    if ctx.reply_to:
        reply_text = ctx.reply_to.text

        if "🗨 لطفاً سوال خود را ارسال کنید." in reply_text:
            await ctx.reply(chat_with_ai(ctx.text), reply_markup=get_back_button())

        elif "📦 لطفاً کد رهگیری مرسوله را ارسال کنید." in reply_text:
            await ctx.reply(track_parcel(ctx.text), reply_markup=get_back_button())

        elif "🌍 لطفاً متن مورد نظر برای ترجمه را ارسال کنید." in reply_text:
            await ctx.reply(translate_to_farsi(ctx.text), reply_markup=get_back_button())

        else:
            await ctx.reply("⚠ دستور نامعتبر! لطفاً از دکمه‌ها استفاده کنید.", reply_markup=get_main_menu())
    else:
        await ctx.reply("⚠ لطفاً ابتدا یک گزینه را انتخاب کنید.", reply_markup=get_main_menu())

# ----------------- اجرای ربات -----------------
app.run()