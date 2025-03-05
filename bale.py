import requests
from datetime import datetime
import jdatetime
from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard

# تنظیمات ربات
bot_token = "‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
bot = Client(bot_token)

# تابع دریافت تاریخ و زمان
def get_time():
    now = datetime.now()
    jalali_date = jdatetime.date.fromgregorian(date=now)
    gregorian_date = now.strftime("%Y-%m-%d")
    islamic_date = jdatetime.date.fromgregorian(date=now).to_islamic().strftime("%Y/%m/%d")  # تاریخ قمری
    time_info = {
        "shamsi_date": jalali_date.strftime("%Y/%m/%d"),
        "gregorian_date": gregorian_date,
        "islamic_date": islamic_date,  # تاریخ قمری
        "time": now.strftime("%H:%M:%S"),
        "day": jalali_date.strftime("%A"),
        "month": jalali_date.strftime("%B"),
        "year": jalali_date.year,
        "day_of_week": jalali_date.strftime("%A")
    }
    return time_info

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
    return "اطلاعات مرسوله پیدا نشد."

# دکمه‌های اینلاین برای منوی اصلی
inline_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("حدیث گو 📖", "hadith")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("دستیار مومن 🤖", "ai_chat")],  # تغییر نام به دستیار مومن
    [("ترجمه به فارسی 📝", "translate"), ("راهنما ❓", "help")],
    [("اطلاعات سازنده 🧑‍💻", "info")]
)

# دکمه برگشت به منو اصلی در حالت چت با هوش مصنوعی
return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])

# دکمه برگشت به منو اصلی
reply_keyboard = ReplyKeyboard(
    ["منوی اصلی 🏠"]
)

# مدیریت پیام‌های ابتدایی
@bot.on_message()
async def on_start(message):
    await message.reply(
        "سلام! به ربات صراط خوش آمدید.\nلطفاً گزینه مورد نظر خود را انتخاب کنید:",
        reply_markup=inline_buttons
    )

# مدیریت انتخاب‌های دکمه‌های اینلاین
@bot.on_callback_query()
async def on_callback(callback_query):
    if callback_query.data == "time":
        time_info = get_time()
        await callback_query.answer(
            f"زمان به وقت ایران:\n\n"
            f"تاریخ شمسی: {time_info['shamsi_date']} 🌸\n"
            f"تاریخ میلادی: {time_info['gregorian_date']} 🌍\n"
            f"تاریخ قمری: {time_info['islamic_date']} 🌙\n"
            f"زمان: {time_info['time']} ⏰\n"
            f"روز: {time_info['day_of_week']} 🗓\n"
            f"ماه: {time_info['month']} 🌙\n"
            f"سال: {time_info['year']} 🎉"
        )
        await callback_query.message.reply(
            "لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            reply_markup=inline_buttons
        )
    elif callback_query.data == "hadith":
        # اضافه کردن دریافت حدیث از API (این قسمت مشابه قبلی است)
        await callback_query.answer("حدیث گو فعال است")
        await callback_query.message.reply(
            "لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            reply_markup=inline_buttons
        )
    elif callback_query.data == "track_parcel":
        await callback_query.answer("لطفاً کد رهگیری مرسوله را وارد کنید.")
        @bot.on_message()
        async def on_message_tracking(message):
            parcel_info = track_parcel(message.text)
            await message.reply(parcel_info, reply_markup=inline_buttons)
    elif callback_query.data == "translate":
        await callback_query.answer("لطفاً متنی که می‌خواهید ترجمه شود را ارسال کنید.")
        @bot.on_message()
        async def on_message_translation(message):
            translation = translate_to_farsi(message.text)  # تابع ترجمه (می‌توانید آن را اضافه کنید)
            await message.reply(translation, reply_markup=inline_buttons)
    elif callback_query.data == "help":
        await callback_query.answer(
            "راهنمای ربات صراط:\n"
            "1. اعلام زمان ⏰: نمایش زمان و تاریخ به شمسی و میلادی\n"
            "2. حدیث گو 📖: دریافت حدیث روز\n"
            "3. دستیار مومن 🤖: چت با دستیار مومن\n"  # تغییر نام به دستیار مومن
            "4. پیگیری مرسوله تیپاکس 📦: پیگیری وضعیت مرسوله\n"
            "5. ترجمه به فارسی 📝: ترجمه متنی به فارسی\n"
            "6. اطلاعات سازنده 🧑‍💻: اطلاعات سازنده ربات"
        )
        await callback_query.message.reply(
            "لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            reply_markup=inline_buttons
        )
    elif callback_query.data == "info":
        await callback_query.answer(
            "ربات صراط توسط تیم توسعه‌دهنده شفق ساخته شده است.\n"
            "برای اطلاعات بیشتر به پیوی ما مراجعه کنید:\n@Devehsan"
        )
        await callback_query.message.reply(
            "لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            reply_markup=inline_buttons
        )
    elif callback_query.data == "ai_chat":
        await callback_query.answer("برای شروع چت با دستیار مومن پیامی ارسال کنید.")
        
        # تعریف تابع برای دریافت پیام و پاسخ از دستیار مومن
        @bot.on_message()
        async def on_message_ai(message):
            # تغییر API URL به آدرس جدید
            url = f"https://momen-api.onrender.com/?text={message.text}"
            response = requests.get(url)
            data = response.json()
            ai_response = data.get("message", "پاسخی از دستیار مومن دریافت نشد.")
            
            await message.reply(ai_response, reply_markup=return_to_main_menu_button)
            await message.reply(
                "برای بازگشت به منوی اصلی، دستور /start را ارسال کنید.",
                reply_markup=return_to_main_menu_button
            )

    elif callback_query.data == "return_to_main_menu":
        await callback_query.answer("به منوی اصلی بازگشتید.")
        await callback_query.message.reply(
            "لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            reply_markup=inline_buttons
        )

# اجرای ربات
bot.run()
