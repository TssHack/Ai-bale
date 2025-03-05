from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard
import requests
from datetime import datetime
import jdatetime
import pytz

# تنظیمات ربات
bot_token = "1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
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
        "year": jalali_date.year,
        "full_time": now.strftime("%A, %d %B %Y, %H:%M:%S")
    }

# تابع دریافت حدیث
def get_hadith():
    try:
        response = requests.get("https://din-esi.onrender.com/random_hadith")
        data = response.json()
        return data.get("hadith", "حدیثی پیدا نشد."), data.get("speaker", "نام سخنران پیدا نشد.")
    except:
        return "مشکلی در دریافت حدیث رخ داد.", "نامشخص"

# تابع چت با هوش مصنوعی
def chat_with_ai(user_message):
    try:
        response = requests.get(f"https://momen-api.onrender.com/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از دستیار مومن دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور هوش مصنوعی رخ داد."

# تابع پیگیری مرسوله تیپاکس
def track_parcel(tracking_code):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/TipaxInfo?code={tracking_code}")
        data = response.json()
        if data["status"]:
            results = data["results"]
            sender = results["sender"]
            receiver = results["receiver"]
            status_info = results["status_info"]
            return f"""📤 فرستنده: {sender['name']} از {sender['city']}
📥 گیرنده: {receiver['name']} در {receiver['city']}
💸 هزینه پستی: {results['package_cost']} تومان
🛳 وزن مرسوله: {results['weight']}
وضعیت‌ها:
{', '.join([f"{status['date']} - {status['status']}" for status in status_info])}"""
        return "اطلاعات مرسوله پیدا نشد."
    except:
        return "مشکلی در دریافت اطلاعات مرسوله رخ داد."

# تابع ترجمه به فارسی
def translate_to_farsi(text):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/GoogleTranslate?text={text}&to=fa")
        data = response.json()
        return data.get("results", "ترجمه‌ای پیدا نشد.")
    except:
        return "مشکلی در ترجمه متن رخ داد."

# تابع دریافت جوک
def get_joke():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/4Jok?page=500")
        data = response.json()
        return data["results"]["post"] if data["status"] else "جوکی پیدا نشد."
    except:
        return "مشکلی در دریافت جوک رخ داد."

# تابع دریافت نرخ طلا و سکه
def get_gold_rate():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/GoldRate")
        data = response.json()
        if data["status"]:
            prices = data["results"]["prices"]
            result = "💰 نرخ طلا و سکه:\n"
            for item in prices:
                name = item["name"]
                price = item["price"]
                sign = "🔺" if item["is_positive"] else "🔻"
                result += f"{name}: {price} ریال {sign}\n"
            return result
        return "نرخ طلا و سکه پیدا نشد."
    except:
        return "مشکلی در دریافت نرخ طلا و سکه رخ داد."

# دکمه‌های اینلاین
inline_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("حدیث گو 📖", "hadith")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel"), ("نرخ طلا و سکه 💰", "gold_rate")],
    [("جوک بگو 😂", "joke"), ("دستیار مومن 🤖", "ai_chat")],
    [("ترجمه به فارسی 📝", "translate"), ("راهنما ❓", "help")],
    [("اطلاعات سازنده 🧑‍💻", "info")]
)

return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])

# مدیریت پیام‌ها
@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if state is None:
        await message.reply("سلام! به ربات صراط خوش آمدید.\nلطفاً گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_buttons)
    elif state == "tracking":
        await message.reply(track_parcel(message.text), reply_markup=inline_buttons)
    elif state == "translate":
        await message.reply(translate_to_farsi(message.text), reply_markup=inline_buttons)
    elif state == "ai_chat":
        await message.reply(chat_with_ai(message.text), reply_markup=return_to_main_menu_button)

    if state != "ai_chat":
        user_states[chat_id] = None

# مدیریت دکمه‌های اینلاین
@bot.on_callback_query()
async def on_callback(callback_query):
    chat_id = callback_query.message.chat.id

    if callback_query.data == "time":
        await callback_query.message.edit_text(str(get_time()), reply_markup=inline_buttons)

    elif callback_query.data == "hadith":
        hadith, speaker = get_hadith()
        await callback_query.message.edit_text(f"📖 {hadith}\n🗣️ {speaker}", reply_markup=inline_buttons)

    elif callback_query.data == "track_parcel":
        user_states[chat_id] = "tracking"
        await callback_query.message.edit_text("لطفاً کد رهگیری را ارسال کنید.")

    elif callback_query.data == "translate":
        user_states[chat_id] = "translate"
        await callback_query.message.edit_text("لطفاً متن خود را ارسال کنید.")

    elif callback_query.data == "ai_chat":
        user_states[chat_id] = "ai_chat"
        await callback_query.message.edit_text("پیام خود را ارسال کنید.")

    elif callback_query.data == "joke":
        await callback_query.message.edit_text(f"😂 {get_joke()}", reply_markup=inline_buttons)

    elif callback_query.data == "gold_rate":
        await callback_query.message.edit_text(get_gold_rate(), reply_markup=inline_buttons)

    elif callback_query.data == "info":
        await callback_query.message.edit_text("ربات توسط تیم شفق ساخته شده است. ارتباط: @Devehsan", reply_markup=inline_buttons)

    elif callback_query.data == "return_to_main_menu":
        user_states[chat_id] = None
        await callback_query.message.edit_text("به منوی اصلی بازگشتید.", reply_markup=inline_buttons)

# اجرای ربات
bot.run()
