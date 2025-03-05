import requests
from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard
from io import BytesIO
from datetime import datetime
import jdatetime

# تنظیمات ربات
bot_token = "‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
bot = Client(bot_token)

# دیکشنری ذخیره وضعیت کاربران
user_states = {}

# تابع دریافت تاریخ و زمان
def get_time():
    now = datetime.now()
    jalali_date = jdatetime.date.fromgregorian(date=now)
    return {
        "shamsi_date": jalali_date.strftime("%Y/%m/%d"),
        "gregorian_date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": jalali_date.strftime("%A"),
        "month": jalali_date.strftime("%B"),
        "year": jalali_date.year,
        "hijri_date": jalali_date.strftime("%Y/%m/%d")
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
            status_details = "\n".join([f"{status['status']} - {status['date']}" for status in status_info])
            return f"""📤 فرستنده: {sender['name']} از {sender['city']}
📥 گیرنده: {receiver['name']} در {receiver['city']}
📦 وضعیت: {status_details}

📦 وزن: {results['weight']}
💰 هزینه کل: {results['total_cost']}
📦 پرداخت: {results['pay_type']}
            """
        return "اطلاعات مرسوله پیدا نشد."
    except:
        return "مشکلی در دریافت اطلاعات مرسوله رخ داد."

# تابع تولید عکس از متن
def generate_image_from_text(query):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/MakePhotoAi?q={query}")
        data = response.json()
        if data["status"]:
            image_url = data["results"]["img"]
            image_response = requests.get(image_url)
            image = BytesIO(image_response.content)  # تبدیل محتوای تصویر به بایت‌استریم
            return image
        return None
    except:
        return None

# تابع دریافت جوک رندوم
def get_joke():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/GoldRate")
        data = response.json()
        if data["status"]:
            return data["results"]["post"]
        return "جوکی پیدا نشد."
    except:
        return "مشکلی در دریافت جوک رخ داد."

# تابع دریافت قیمت طلا و سکه
def get_gold_rate():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/GoldRate")
        data = response.json()
        if data["status"]:
            prices = data["results"]["prices"]
            gold_info = "\n".join([f"💰 {item['name']}: {item['price']} ریال (تغییر: {item['change_value']} ریال, {item['change_percent']}%)"
                                  for item in prices])
            return f"📊 قیمت طلا و سکه:\n{gold_info}"
        return "قیمت طلا و سکه پیدا نشد."
    except:
        return "مشکلی در دریافت قیمت طلا و سکه رخ داد."

# دکمه‌های اینلاین
inline_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("حدیث گو 📖", "hadith")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("دستیار مومن 🤖", "ai_chat")],
    [("ترجمه به فارسی 📝", "translate"), ("تولید عکس 🖼️", "generate_image")],
    [("جوک رندوم 😂", "get_joke"), ("قیمت طلا و سکه 💰", "gold_rate")],
    [("راهنما ❓", "help")],
    [("اطلاعات سازنده 🧑‍💻", "info")]
)

return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])
reply_keyboard = ReplyKeyboard(["منوی اصلی 🏠"])

# مدیریت پیام‌های ابتدایی
@bot.on_message()
async def on_start(message):
    user_states[message.chat.id] = None  # ریست وضعیت کاربر
    await message.reply("سلام! به ربات صراط خوش آمدید.\nلطفاً گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_buttons)

# مدیریت دکمه‌های اینلاین
@bot.on_callback_query()
async def on_callback(callback_query):
    chat_id = callback_query.message.chat.id

    if callback_query.data == "time":
        time_info = get_time()
        await callback_query.message.edit_text(
            f"""🕰️ زمان:
{time_info['time']}
📆 تاریخ شمسی: {time_info['shamsi_date']}
🌍 تاریخ میلادی: {time_info['gregorian_date']}
🌙 تاریخ قمری: {time_info['hijri_date']}
📅 روز هفته: {time_info['day']}
🗓 ماه: {time_info['month']}
📅 سال: {time_info['year']}""",
            reply_markup=inline_buttons
        )

    elif callback_query.data == "hadith":
        hadith, speaker = get_hadith()
        await callback_query.message.edit_text(f"📖 حدیث:\n{hadith}\n🗣️ {speaker}", reply_markup=inline_buttons)

    elif callback_query.data == "track_parcel":
        user_states[chat_id] = "tracking"
        await callback_query.message.edit_text("لطفاً کد رهگیری را ارسال کنید.")

    elif callback_query.data == "translate":
        user_states[chat_id] = "translate"
        await callback_query.message.edit_text("لطفاً متن مورد نظر را ارسال کنید.")

    elif callback_query.data == "ai_chat":
        user_states[chat_id] = "ai_chat"
        await callback_query.message.edit_text("پیام خود را ارسال کنید تا پاسخ دریافت کنید.")

    elif callback_query.data == "generate_image":
        user_states[chat_id] = "generate_image"
        await callback_query.message.edit_text("لطفاً کلمه‌ای را وارد کنید تا تصویر تولید شود.")

    elif callback_query.data == "get_joke":
        joke = get_joke()
        await callback_query.message.edit_text(joke, reply_markup=inline_buttons)

    elif callback_query.data == "gold_rate":
        gold_rate = get_gold_rate()
        await callback_query.message.edit_text(gold_rate, reply_markup=inline_buttons)

    elif callback_query.data == "help":
        await callback_query.message.edit_text("راهنمای ربات:\n1. اعلام زمان\n2. حدیث روز\n3. چت با دستیار مومن\n4. پیگیری مرسوله تیپاکس\n5. ترجمه به فارسی\n6. تولید عکس\n7. جوک رندوم\n8. قیمت طلا و سکه\n9. اطلاعات سازنده", reply_markup=inline_buttons)

    elif callback_query.data == "info":
        await callback_query.message.edit_text("ربات توسط تیم شفق ساخته شده است. ارتباط: @Devehsan", reply_markup=inline_buttons)

    elif callback_query.data == "return_to_main_menu":
        user_states[chat_id] = None
        await callback_query.message.edit_text("به منوی اصلی بازگشتید.", reply_markup=inline_buttons)

# پردازش ورودی کاربران
@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if state == "tracking":
        response = track_parcel(message.text)
        await message.reply(response, reply_markup=inline_buttons)
    elif state == "translate":
        response = translate_to_farsi(message.text)
        await message.reply(response, reply_markup=inline_buttons)
    elif state == "ai_chat":
        response = chat_with_ai(message.text)
        await message.reply(response)
    elif state == "generate_image":
        image = generate_image_from_text(message.text)
        if image:
            await message.reply_photo(image, caption="تصویر تولید شده:", reply_markup=inline_buttons)
        else:
            await message.reply("متاسفانه تصویری تولید نشد.", reply_markup=inline_buttons)

    # ریست وضعیت کاربر بعد از پردازش پیام (اگر نه در حالت چت هوش مصنوعی نباشد)
    if state != "ai_chat":
        user_states[chat_id] = None  # ریست وضعیت کاربر بعد از پردازش پیام

# اجرای ربات
bot.run()
