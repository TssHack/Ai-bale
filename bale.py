import json
import locale
from convertdate import islamic
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

def load_events(year):
    try:
        with open(f"events_{year}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_today_event(jalali_date):
    events = load_events(jalali_date.year)
    date_key = f"{jalali_date.month:02}/{jalali_date.day:02}"
    return events.get(date_key, "مناسبتی ثبت نشده است")

def get_time():
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.now(iran_tz)

    jalali_date = jdatetime.date.fromgregorian(year=now.year, month=now.month, day=now.day)
    hijri_date = islamic.from_gregorian(now.year, now.month, now.day)
    hijri_date_str = f"{hijri_date[2]:02}/{hijri_date[1]:02}/{hijri_date[0]}"

    eid_date = jdatetime.date(jalali_date.year + 1, 1, 1)
    remaining_days = (eid_date - jalali_date).days

    today_event = get_today_event(jalali_date)

    return {
        "shamsi_date": jalali_date.strftime("%Y/%m/%d"),
        "gregorian_date": now.strftime("%Y-%m-%d"),
        "hijri_date": hijri_date_str,
        "time": now.strftime("%H:%M:%S"),
        "day": jalali_date.strftime("%A"),
        "month": jalali_date.strftime("%B"),
        "year": jalali_date.year,
        "remaining_days": remaining_days,
        "event": today_event
    }

# تابع دریافت حدیث
def get_hadith():
    try:
        response = requests.get("https://din-esi.onrender.com/random_hadith")
        data = response.json()
        return data.get("hadith", "حدیثی پیدا نشد."), data.get("speaker", "نام سخنران پیدا نشد.")
    except:
        return "مشکلی در دریافت حدیث رخ داد.", "نامشخص"

def get_fact():
    try:
        response = requests.get("https://fact-api.onrender.com/f")
        data = response.json()
        return data.get("fact", "دانستی پیدا نشد."), data.get("source", "منبع پیدا نشد.")
    except:
        return "مشکلی در دریافت دانستنی رخ داد.", "نامشخص"

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

# ترجمه متن
def get_translate(text):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/GoogleTranslate?text={text}&to=fa")
        data = response.json()
        return data.get("results", "ترجمه‌ای پیدا نشد.")
    except:
        return "مشکلی در ترجمه رخ داد."

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
        
        # ساخت پیام کامل با اطلاعات بیشتر
        parcel_info = f"📤فرستنده: {sender['name']} از {sender['city']}\n"
        parcel_info += f"🏢تعداد ارسال‌ها: {results['dispatch_count']}\n"
        parcel_info += f"💰هزینه پست: {results['package_cost']} تومان\n"
        parcel_info += f"📦نوع بسته: {results['COD']}\n"
        parcel_info += f"🚚وزن: {results['weight']} کیلوگرم\n"
        parcel_info += f"💸هزینه کل: {results['total_cost']} تومان\n"
        parcel_info += f"🔄وضعیت پرداخت: {results['pay_type']}\n"
        parcel_info += f"🌍مسافت: {results['city_distance']} کیلومتر\n"
        parcel_info += f"📍زون: {results['distance_zone']}\n"
        
        parcel_info += f"\n📥گیرنده: {receiver['name']} در {receiver['city']}\n"
        
        for status in status_info:
            parcel_info += f"\n📝تاریخ: {status['date']}\n"
            parcel_info += f"🔹وضعیت: {status['status']}\n"
            parcel_info += f"📍محل: {status['representation']}\n"
        
        return parcel_info
    return "🔮اطلاعات مرسوله پیدا نشد."

def get_joke():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/4Jok")
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

# تنظیم منطقه به فارسی
locale.setlocale(locale.LC_TIME, 'fa_IR')

def calculate_age(birthdate_text):
    try:
        # تبدیل تاریخ شمسی به میلادی
        birthdate_jalali = jdatetime.datetime.strptime(birthdate_text, "%Y/%m/%d")
        birthdate = birthdate_jalali.togregorian()  # تبدیل به میلادی
    except ValueError:
        return "⚠ فرمت تاریخ اشتباه است. لطفاً به صورت YYYY/MM/DD شمسی وارد کنید."

    # محاسبه سن
    today = datetime.today()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1

    # تبدیل تاریخ تولد به شمسی
    birthdate_jalali = jdatetime.date.fromgregorian(date=birthdate)

    # محاسبه تعداد روزهای گذشته و تا تولد بعدی
    days_since_birth = (today - birthdate).days
    next_birthday = datetime(today.year, birthdate.month, birthdate.day)
    if today > next_birthday:
        next_birthday = datetime(today.year + 1, birthdate.month, birthdate.day)
    days_until_next_birthday = (next_birthday - today).days

    # روز هفته تولد
    birth_weekday = birthdate.strftime('%A')  # نام روز هفته به انگلیسی
    # تبدیل نام روز هفته به فارسی
    weekdays_farsi = {
        'Monday': 'دوشنبه',
        'Tuesday': 'سه‌شنبه',
        'Wednesday': 'چهارشنبه',
        'Thursday': 'پنج‌شنبه',
        'Friday': 'جمعه',
        'Saturday': 'شنبه',
        'Sunday': 'یکشنبه'
    }
    birth_weekday_farsi = weekdays_farsi.get(birth_weekday, birth_weekday)

    # محاسبه عدد شمع تولد
    birth_number = sum([int(digit) for digit in str(birthdate.year)])

    return f"""
🌟 **اطلاعات سن شما** 🌟

📅 **تاریخ تولد:** {birthdate.strftime('%Y-%m-%d')} (میلادی)
📆 **تاریخ تولد (شمسی):** {birthdate_jalali.strftime('%Y/%m/%d')} (شمسی)

🎂 **سن شما:** {age} سال
🗓️ **تعداد روزهای گذشته از تولد شما:** {days_since_birth} روز
🔮 **تعداد روزهای باقی‌مانده تا تولد بعدی شما:** {days_until_next_birthday} روز

📅 **روز هفته تولد شما:** {birth_weekday_farsi}

🕰️ **تاریخ امروز:** {today.strftime('%Y-%m-%d')} (میلادی)

🔢 **عدد شمع تولد شما:** {birth_number}
"""
    return result
    
# دکمه‌های اینلاین
inline_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("حدیث گو 📖", "hadith")],
    [("دریافت نرخ طلا و سکه 💰", "gold_rate")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("دستیار مومن 🤖", "ai_chat")],
    [("ترجمه 📝", "translate"), ("جوک تصادفی 😂", "random_joke")],
    [("وکیل ⚖️", "lawyer")],
    [("روانشناس 🧠", "psychologist")],
    [("محاسبه سن 🎂", "calculate_age")],
    [("دانستنی‌ها 🧠", "facts")],
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

    elif state == "get_translate":
        translation = get_translate(message.text)
        await message.reply(f"📜 **متن ترجمه‌شده:**\n{translation}", reply_markup=inline_buttons)
        user_states[chat_id] = None  

    elif state == "get_birthdate":
        response = calculate_age(message.text.strip())
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
            f"""
🕰 **زمان دقیق:** {time_info['time']}
📆 **تاریخ شمسی:** {time_info['shamsi_date']}
🌍 **تاریخ میلادی:** {time_info['gregorian_date']}
🌙 **تاریخ قمری:** {time_info['hijri_date']}
📅 **روز:** {time_info['day']}
🍂 **ماه شمسی:** {time_info['month']}
🎯 **روزهای باقی‌مانده تا عید نوروز:** {time_info['remaining_days']} روز
✨ **مناسبت روز:** {time_info['event']}
""",
            reply_markup=inline_buttons
        )

    elif callback_query.data == "calculate_age":
        user_states[chat_id] = "get_birthdate"
        await callback_query.message.edit_text("🎂 لطفاً تاریخ تولد خود را به صورت YYYY-MM-DD وارد کنید:")

    elif callback_query.data == "hadith":
        hadith, speaker = get_hadith()
        await callback_query.message.edit_text(f"📖 **حدیث:**\n{hadith}\n🗣️ **{speaker}**", reply_markup=inline_buttons)

    elif callback_query.data == "facts":
        fact, source = get_fact()
        await callback_query.message.edit_text(f"📌 **فکت:**\n{fact}\n✏️ **{source}**", reply_markup=inline_buttons)

    elif callback_query.data == "track_parcel":
        user_states[chat_id] = "tracking"
        await callback_query.message.edit_text("📦 لطفاً **کد رهگیری** را ارسال کنید:")

    elif callback_query.data == "ai_chat":
        user_states[chat_id] = "ai_chat"
        await callback_query.message.edit_text("🤖 پیام خود را برای دستیار مومن ارسال کنید:")

    elif callback_query.data == "translate":
        user_states[chat_id] = "get_translate"
        await callback_query.message.edit_text("📜 لطفاً متنی مورد نظر برای ترجمه به فارسی را ارسال کنید:")
        
    elif callback_query.data == "random_joke":
        await callback_query.message.edit_text(get_joke(), reply_markup=inline_buttons)

    elif callback_query.data == "gold_rate":
        await callback_query.message.edit_text(get_gold_rate(), reply_markup=inline_buttons)

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
