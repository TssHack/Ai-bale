from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard
import requests
from datetime import datetime
import jdatetime
import pytz

# تنظیمات ربات
bot_token = "‏‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
bot = Client(bot_token)

# دیکشنری ذخیره وضعیت کاربران
user_states = {}

# تابع دریافت تاریخ و زمان به وقت ایران
def get_time():
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.now(iran_tz)
    jalali_date = jdatetime.date.fromgregorian(date=now)
    return {
        "shamsi_date": jalali_date.strftime("%Y/%m/%d"),
        "gregorian_date": now.strftime("%Y-%m-%d"),
        "hijri_date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S"),
        "day": jalali_date.strftime("%A"),
        "month": jalali_date.strftime("%B"),
        "year": jalali_date.year
    }

# تابع دریافت حدیث
def get_hadith():
    try:
        response = requests.get("https://din-esi.onrender.com/random_hadith")
        data = response.json()
        return data.get("hadith", "حدیثی پیدا نشد."), data.get("speaker", "نام سخنران پیدا نشد.")
    except:
        return "مشکلی در دریافت حدیث رخ داد.", "نامشخص"

# تابع چت با هوش مصنوعی اسلامی
def chat_with_ai(user_message):
    try:
        response = requests.get(f"https://momen-api.onrender.com/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از دستیار مومن دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور هوش مصنوعی رخ داد."

# تابع چت با وکیل هوش مصنوعی
def chat_with_lawyer(user_message):
    try:
        response = requests.get(f"https://vakil-xspt.onrender.com/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از وکیل دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور وکیل رخ داد."

# تابع چت با روانشناس هوش مصنوعی
def chat_with_psychologist(user_message):
    try:
        response = requests.get(f"https://ravan-ehsan.onrender.com/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از روانشناس دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور روانشناسی رخ داد."

# تابع پیگیری مرسوله تیپاکس
def track_parcel(tracking_code):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/TipaxInfo?code={tracking_code}")
        data = response.json()
        if data["status"]:
            results = data["results"]
            return f"""📦 **پیگیری مرسوله تیپاکس**
            
📤 **فرستنده:** {results['sender']['name']} از {results['sender']['city']}
📥 **گیرنده:** {results['receiver']['name']} در {results['receiver']['city']}
🚚 **وضعیت مرسوله:** {', '.join([f"{status['date']} - {status['status']}" for status in results['status_info']])}
"""
        return "❌ اطلاعات مرسوله پیدا نشد. لطفاً کد را بررسی کنید."
    except:
        return "مشکلی در دریافت اطلاعات مرسوله رخ داد."

# دکمه‌های اینلاین
inline_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("حدیث گو 📖", "hadith")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("دستیار مومن 🤖", "ai_chat")],
    [("وکیل ⚖️", "lawyer")],
    [("روانشناس 🧠", "psychologist")],
    [("راهنما ❓", "help"), ("اطلاعات سازنده 🧑‍💻", "info")]
)

return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])

# مدیریت پیام‌ها
@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if state is None:
        await message.reply("🤖 به ربات صراط خوش آمدید!\n\n✨ دستیار هوشمند اسلامی شما ✨\n\n📌 این ربات امکانات متنوعی را در اختیار شما قرار می‌دهد:", reply_markup=inline_buttons)

    elif state == "tracking":
        tracking_code = message.text.strip()
        response = track_parcel(tracking_code)
        await message.reply(response, reply_markup=inline_buttons)
        user_states[chat_id] = None  

    elif state == "ai_chat":
        response = chat_with_ai(message.text)
        await message.reply(response, reply_markup=return_to_main_menu_button)

    elif state == "lawyer":
        response = chat_with_lawyer(message.text)
        await message.reply(response, reply_markup=return_to_main_menu_button)

    elif state == "psychologist":
        response = chat_with_psychologist(message.text)
        await message.reply(response, reply_markup=return_to_main_menu_button)

    if state not in ["ai_chat", "lawyer", "psychologist"]:
        user_states[chat_id] = None  

# مدیریت دکمه‌های اینلاین
@bot.on_callback_query()
async def on_callback(callback_query):
    chat_id = callback_query.message.chat.id

    if callback_query.data == "time":
        time_info = get_time()
        await callback_query.message.edit_text(
            f"""🕰 **زمان دقیق:** {time_info['time']}
📆 **تاریخ شمسی:** {time_info['shamsi_date']}
🌍 **تاریخ میلادی:** {time_info['gregorian_date']}
🌙 **تاریخ قمری:** {time_info['hijri_date']}
""",
            reply_markup=inline_buttons
        )

    elif callback_query.data == "hadith":
        hadith, speaker = get_hadith()
        await callback_query.message.edit_text(f"📖 **حدیث:**\n{hadith}\n🗣️ **{speaker}**", reply_markup=inline_buttons)

    elif callback_query.data == "track_parcel":
        user_states[chat_id] = "tracking"
        await callback_query.message.edit_text("📦 لطفاً **کد رهگیری** را ارسال کنید:")

    elif callback_query.data == "ai_chat":
        user_states[chat_id] = "ai_chat"
        await callback_query.message.edit_text("🤖 پیام خود را برای دستیار مومن ارسال کنید:")

    elif callback_query.data == "lawyer":
        user_states[chat_id] = "lawyer"
        await callback_query.message.edit_text("⚖️ پیام خود را برای وکیل ارسال کنید:")

    elif callback_query.data == "psychologist":
        user_states[chat_id] = "psychologist"
        await callback_query.message.edit_text("🧠 پیام خود را برای روانشناس ارسال کنید:")

    elif callback_query.data == "help":
        await callback_query.message.edit_text("❓ **راهنمای ربات صراط** ❓\n\n🔹 برای استفاده از امکانات، یکی از گزینه‌های منو را انتخاب کنید.\n🔹 هر بخش دارای قابلیت‌های منحصربه‌فردی است که می‌توانید از آن بهره ببرید.\n\n📌 در صورت نیاز به راهنمایی بیشتر، با پشتیبانی در ارتباط باشید.", reply_markup=inline_buttons)

    elif callback_query.data == "info":
        await callback_query.message.edit_text("🧑‍💻 این ربات با افتخار توسط **احسان فضلی** و تیم **شفق** توسعه یافته است.\n\n🔹 ارائه‌دهنده خدمات هوش مصنوعی و ابزارهای کاربردی اسلامی 🔹", reply_markup=inline_buttons)

    elif callback_query.data == "return_to_main_menu":
        user_states[chat_id] = None
        await callback_query.message.edit_text("🏠 بازگشت به منوی اصلی:", reply_markup=inline_buttons)

# اجرای ربات
bot.run()
