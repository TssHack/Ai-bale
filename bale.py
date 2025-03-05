from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard
import requests
from datetime import datetime
import jdatetime
import pytz
import json

# تنظیمات ربات
bot_token = "‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
bot = Client(bot_token)

# وضعیت کاربران
user_states = {}

# ذخیره وضعیت کاربران در فایل JSON
def save_states():
    with open("states.json", "w") as file:
        json.dump(user_states, file)

def load_states():
    try:
        with open("states.json", "r") as file:
            return json.load(file)
    except:
        return {}

user_states = load_states()

# تابع دریافت تاریخ و زمان
def get_time():
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.now(iran_tz)
    jalali_date = jdatetime.date.fromgregorian(date=now)
    return f"""🕰️ **اعلام زمان:**

📆 **تاریخ شمسی:** {jalali_date.strftime("%Y/%m/%d")}
🌍 **تاریخ میلادی:** {now.strftime("%Y-%m-%d")}
🌙 **تاریخ قمری:** {now.strftime("%d/%m/%Y")}

⏰ **ساعت:** {now.strftime("%H:%M:%S")}
📅 **روز هفته:** {jalali_date.strftime("%A")}
"""

# دریافت حدیث
def get_hadith():
    try:
        response = requests.get("https://din-esi.onrender.com/random_hadith")
        data = response.json()
        return f"📖 {data.get('hadith', 'حدیثی پیدا نشد.')}\n🗣️ {data.get('speaker', 'نامشخص')}"
    except:
        return "❌ مشکلی در دریافت حدیث رخ داد."

# جوک
def get_joke():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/4Jok?page=500")
        data = response.json()
        return f"😂 {data['results']['post']}"
    except:
        return "❌ مشکلی در دریافت جوک رخ داد."

# نرخ طلا و سکه
def get_gold_rate():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/GoldRate")
        data = response.json()
        prices = data["results"]["prices"]
        text = "💰 **نرخ طلا و سکه:**\n\n"
        for item in prices:
            change = "🔺" if item["is_positive"] else "🔻"
            text += f"{item['name']}: {item['price']} ریال ({change} {item['change_value']})\n"
        return text
    except:
        return "❌ مشکلی در دریافت نرخ طلا و سکه رخ داد."

# نرخ ارز
def get_currency():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/Currency")
        data = response.json()
        rates = data["results"]["prices"]
        text = "💵 **نرخ ارز:**\n\n"
        for item in rates:
            change = "🔺" if item["is_positive"] else "🔻"
            text += f"{item['name']}: {item['price']} ریال ({change} {item['change_value']})\n"
        return text
    except:
        return "❌ مشکلی در دریافت نرخ ارز رخ داد."

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
            return f"""📦 **پیگیری مرسوله:**

📤 **فرستنده:** {sender['name']} از {sender['city']}
📥 **گیرنده:** {receiver['name']} در {receiver['city']}
💳 **هزینه:** {results['total_cost']} تومان
🛳 **وزن:** {results['weight']} کیلوگرم

🚦 **وضعیت‌ها:**
{', '.join([f"{status['date']} - {status['status']}" for status in status_info])}"""
        return "❌ کد رهگیری نامعتبر است."
    except:
        return "❌ مشکلی در دریافت اطلاعات مرسوله رخ داد."

# دکمه‌ها
inline_buttons = InlineKeyboard(
    [("🕰️ اعلام زمان", "time"), ("📖 حدیث گو", "hadith")],
    [("😂 جوک بگو", "joke"), ("💰 نرخ طلا و سکه", "gold_rate")],
    [("💵 نرخ ارز", "currency")],
    [("📦 پیگیری مرسوله تیپاکس", "track_parcel"), ("🔄 ریستارت", "restart")],
    [("🧑‍💻 اطلاعات سازنده", "info")]
)

reply_keyboard = ReplyKeyboard(["🏠 منوی اصلی"])

# پیام‌های دریافتی
@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(str(chat_id))

    if state == "tracking":
        await message.reply("🔍 لطفاً کد رهگیری خود را ارسال کنید.", reply_markup=inline_buttons)
    else:
        await message.reply("سلام! 😊 لطفاً گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_buttons)

    user_states[str(chat_id)] = None
    save_states()

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

    elif callback_query.data == "currency":
        await callback_query.message.edit_text(get_currency(), reply_markup=inline_buttons)

    elif callback_query.data == "track_parcel":
        user_states[str(chat_id)] = "tracking"
        await callback_query.message.edit_text("🔍 لطفاً کد رهگیری خود را ارسال کنید.", reply_markup=inline_buttons)

    elif callback_query.data == "restart":
        user_states[str(chat_id)] = None
        await callback_query.message.edit_text("✅ ربات با موفقیت ریست شد.", reply_markup=inline_buttons)

    elif callback_query.data == "info":
        await callback_query.message.edit_text("👨‍💻 این ربات توسط تیم شفق ساخته شده است.\nارتباط: @Devehsan", reply_markup=inline_buttons)

    save_states()

# اجرای ربات
print("✅ ربات با موفقیت شروع شد!")
bot.run()
