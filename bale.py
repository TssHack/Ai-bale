from balethon.objects import InlineKeyboard, ReplyKeyboard
from fonc import chat_with_ai_api, chat_with_ai, chat_with_lawyer, chat_with_psychologist, get_gpt, get_translate, load_events, get_today_event, get_time, convert_to_fonts, calculate_age, get_gold_rate, get_weather, get_fot, track_parcel, mobile, aparat, digikala, music, get_hadith, get_joke, get_fact, get_wise_quote, get_zekr
from balethon import Client
from info import bot_token

# تنظیمات ربات
bot = Client(bot_token)

# دیکشنری ذخیره وضعیت کاربران
user_states = {}
    
# دکمه‌های اینلاین
inline_buttons = InlineKeyboard(
    [("🤖 بخش هوش مصنوعی", "ai_services")],
    [("📌 بخش کاربردی و ابزاری", "tools")],
    [("🎯 بخش سرگرمی و علمی", "fun_science")],
    [("ℹ️ درباره ما", "info"), ("راهنما 🧬", "help")]
)

tools_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time")],
    [("اوقات شرعی 🌆", "shar"],
    [("فونت ساز 🦄", "font")],
    [("محاسبه سن 🎂", "calculate_age")],
    [("دریافت نرخ طلا و سکه 💰", "gold_rate")],
    [("وضعیت آب و هوا ⛅️", "w_i")],
    [("بازی های امروز ⚽️", "fot")],
    [("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("جستجوی گوشی 📱", "mobi")],
    [("جستجو در آپارات 🎥", "apa")],
    [("جستجو در دیجی کالا 🗣️", "kala")],
    [("جستجو خواننده 🎵", "mu")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

fun_science_buttons = InlineKeyboard(
    [("حدیث 📖", "hadith")],
    [("جوک تصادفی 😂", "random_joke")],
    [("دانستنی 🧠", "fact")],
    [("سخن بزرگان 🗣️", "so")],
    [("ذکر هفته 📿", "zekr")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)
                  
ai_services_buttons = InlineKeyboard(
    [("هوش مصنوعی حافظه دار 🧠", "gpt1")],
    [("دستیار مومن 🤖", "ai_chat")],
    [("وکیل ⚖️", "lawyer"), ("روانشناس 🧠", "psychologist")],
    [("ChatGPT-4o 🧩", "gpt")],
    [("مترجم انگلیسی 📝", "translate")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])
#join = InlineKeyboard([InlineKeyboardButton("🔗 عضویت در کانال", url="https://ble.ir/shafag_tm")])
Ai_back = InlineKeyboard([("🔙", "Ai_b")])

#@bot.on_message(~is_joined(CHANNEL_ID))
#async def not_joined(message):
    # اگر کاربر عضو کانال نباشد
    #await message.reply("🚫 برای استفاده از ربات، ابتدا در کانال ما عضو شوید.\nسپس دستور /start را وارد کنید.", reply_markup=join)


@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    if state is None:
       await message.reply("🤖 به ربات صراط خوش آمدید!\n\n✨ دستیار هوشمند اسلامی شما ✨\n\n📌 این ربات امکانات متنوعی را در اختیار شما قرار می‌دهد:", reply_markup=inline_buttons)
    elif state == "tracking":
        await bot.send_chat_action(chat_id, "typing") 
        tracking_code = message.text.strip()
        response = track_parcel(tracking_code)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None 

    elif state == "shary":
        await bot.send_chat_action(chat_id, "typing") 
        city = message.text.strip()
        response = get_prayer_times(city)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None 

    elif state == "fontt":
        await bot.send_chat_action(chat_id, "typing")
        text = message.text.strip()
        response = convert_to_fonts(text)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "get_weather":
        await bot.send_chat_action(chat_id, "typing") 
        city = message.text.strip()
        response = get_weather(city)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None  

    elif state == "s-m":
        await bot.send_chat_action(chat_id, "typing") 
        mo = message.text.strip()
        response = mobile(mo)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "s-a":
        await bot.send_chat_action(chat_id, "typing") 
        query = message.text.strip()
        response = aparat(query)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "s-mu":
        await bot.send_chat_action(chat_id, "typing")
        query = message.text.strip()
        response = music(query)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "s-d":
        await bot.send_chat_action(chat_id, "typing")
        query = message.text.strip()
        response = digikala(query)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "get_translate":
        await bot.send_chat_action(chat_id, "typing")
        translation = get_translate(message.text)
        await message.reply(f"📜 **متن ترجمه‌شده:**\n{translation}", reply_markup=ai_services_buttons)
        user_states[chat_id] = None  

    elif state == "get_birthdate":
        await bot.send_chat_action(chat_id, "typing") 
        response = calculate_age(message.text.strip())
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None  

    elif state == "ai_chat":
        await bot.send_chat_action(chat_id, "typing")  # اصلاح شد
        response = chat_with_ai(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state == "gpt-1":
        await bot.send_chat_action(chat_id, "typing")
        user_id = message.chat.id  # شناسه کاربر را از پیام دریافت می‌کنید
        query = message.text
        response = chat_with_ai_api(query, user_id)  # ارسال پیام کاربر و شناسه به تابع
        await message.reply(response, reply_markup=Ai_back)

    elif state == "gpt-chat":
        await bot.send_chat_action(chat_id, "typing")
        response = get_gpt(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state == "lawyer":
        await bot.send_chat_action(chat_id, "typing")
        response = chat_with_lawyer(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state == "psychologist":
        await bot.send_chat_action(chat_id, "typing")
        response = chat_with_psychologist(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state not in ["ai_chat", "lawyer", "psychologist", "gpt-chat", "gpt-1"]:
        user_states[chat_id] = None  

# مدیریت دکمه‌های اینلاین
@bot.on_callback_query()
async def on_callback(callback_query):
    chat_id = callback_query.message.chat.id

    if callback_query.data == "tools":
        await callback_query.message.edit_text("🔧 **بخش کاربردی و ابزاری**", reply_markup=tools_buttons)

    elif callback_query.data == "fun_science":
        await callback_query.message.edit_text("🎯 **بخش سرگرمی و علمی**", reply_markup=fun_science_buttons)

    elif callback_query.data == "ai_services":
        await callback_query.message.edit_text("🤖 **بخش هوش مصنوعی**", reply_markup=ai_services_buttons)

    elif callback_query.data == "return_to_main_menu":
        user_states[chat_id] = None
        await callback_query.message.edit_text("🏠 **منوی اصلی:**", reply_markup=inline_buttons)

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
            reply_markup=tools_buttons
        )

    elif callback_query.data == "calculate_age":
        user_states[chat_id] = "get_birthdate"
        await callback_query.message.edit_text("🎂 لطفاً تاریخ تولد خود را به صورت فرمت YYYY/MM/DD (سال/ماه/روز) وارد کنید. برای مثال : 1374/2/4")

    elif callback_query.data == "font":
        user_states[chat_id] = "fontt"
        await callback_query.message.edit_text("🧩 متن انگلیسی مورد نظر برای ایجاد فونت را ارسال کنید.") 

    elif callback_query.data == "hadith":
        hadith, speaker = get_hadith()
        await callback_query.message.edit_text(f"📖 **حدیث:**\n{hadith}\n🗣️ **{speaker}**", reply_markup=fun_science_buttons)

    elif callback_query.data == "fact":
        fact, source = get_fact()
        await callback_query.message.edit_text(f"📌 **فکت:**\n{fact}\n**موضوع**✏️ (**{source}**)", reply_markup=fun_science_buttons)

    elif callback_query.data == "track_parcel":
        user_states[chat_id] = "tracking"
        await callback_query.message.edit_text("📦 لطفاً **کد رهگیری** را ارسال کنید:")

    elif callback_query.data == "ai_chat":
        user_states[chat_id] = "ai_chat"
        await callback_query.message.edit_text("🤖 **پیام خود را برای دستیار مومن ارسال کنید:**")

    elif callback_query.data == "gpt":
        user_states[chat_id] = "gpt-chat"
        await callback_query.message.edit_text("🧩 **پیام خود را برای ChatGPT-4o بفرستید :**")

    elif callback_query.data == "gpt1":
        user_states[chat_id] = "gpt-1"
        await callback_query.message.edit_text("🧬 **پیام خود را برای هوش مصنوعی بفرستید👀 :**")

    elif callback_query.data == "translate":
        user_states[chat_id] = "get_translate"
        await callback_query.message.edit_text("**📜 لطفاً متنی مورد نظر برای ترجمه به فارسی را ارسال کنید:**")
        
    elif callback_query.data == "random_joke":
        await callback_query.message.edit_text(get_joke(), reply_markup=fun_science_buttons)

    elif callback_query.data == "fot":
        await callback_query.message.edit_text(get_fot(), reply_markup=tools_buttons)

    elif callback_query.data == "gold_rate":
        await callback_query.message.edit_text(get_gold_rate(), reply_markup=tools_buttons)

    elif callback_query.data == "so":
        await callback_query.message.edit_text(get_wise_quote(), reply_markup=fun_science_buttons) 

    elif callback_query.data == "zekr":
        await callback_query.message.edit_text(get_zekr(), reply_markup=fun_science_buttons)   

    elif callback_query.data == "lawyer":
        user_states[chat_id] = "lawyer"
        await callback_query.message.edit_text("⚖️ **پیام خود را برای وکیل ارسال کنید:**")

    elif callback_query.data == "psychologist":
        user_states[chat_id] = "psychologist"
        await callback_query.message.edit_text("🧠 **پیام خود را برای روانشناس ارسال کنید:**")

    elif callback_query.data == "help":
        await callback_query.message.edit_text("❓ **راهنمای ربات صراط** ❓\n\n🔹 برای استفاده از امکانات، یکی از گزینه‌های منو را انتخاب کنید.\n🔹 هر بخش دارای قابلیت‌های منحصربه‌فردی است که می‌توانید از آن بهره ببرید.\n\n📌 در صورت نیاز به راهنمایی بیشتر، با پشتیبانی در ارتباط باشید.\n👨‍💻 @Devehsan", reply_markup=inline_buttons)

    elif callback_query.data == "info":
        await callback_query.message.edit_text("🧑‍💻 این ربات با افتخار توسط **احسان فضلی** و تیم **شفق** توسعه یافته است.\n\n🔹 ارائه‌دهنده خدمات هوش مصنوعی و ابزارهای کاربردی اسلامی 🔹", reply_markup=inline_buttons)

    elif callback_query.data == "return_to_main_menu":
         user_states[chat_id] = None
         await callback_query.message.edit_text("🤖 به ربات صراط خوش آمدید!\n\n✨ دستیار هوشمند اسلامی شما ✨\n\n📌 این ربات امکانات متنوعی را در اختیار شما قرار می‌دهد:", reply_markup=inline_buttons)

    elif callback_query.data == "w_i":
        user_states[chat_id] = "get_weather"
        await callback_query.message.edit_text("🌆 لطفا نام شهر خود را ارسال کنید :")

    elif callback_query.data == "shar":
        user_states[chat_id] = "shary"
        await callback_query.message.edit_text("🌆 لطفا نام شهر خود را ارسال کنید :")

    elif callback_query.data == "mobi":
        user_states[chat_id] = "s-m"
        await callback_query.message.edit_text("**🔎📱 لطفا نام موبایل مورد نظر خود را ارسال کنید:**")

    elif callback_query.data == "mu":
        user_states[chat_id] = "s-mu"
        await callback_query.message.edit_text("**🔎🎵لطفا نام خواننده مورد نظر را ارسال کنید:**")
        
    elif callback_query.data == "apa":
        user_states[chat_id] = "s-a"
        await callback_query.message.edit_text("**🔎🎥 موضوع مورد نظر برای جستجو را ارسال کنید:**")

    elif callback_query.data == "kala":
        user_states[chat_id] = "s-d"
        await callback_query.message.edit_text("**🔎💢نام کلای مورد نظر برای جستجو در دیجی کالا را ارسال کنید:**")

    elif callback_query.data == "Ai_b":
        user_states[chat_id] = None
        await callback_query.message.edit_text("👀به بخش هوش مصنوعی برگشتید", reply_markup= ai_services_buttons)
# اجرای ربات
bot.run()
