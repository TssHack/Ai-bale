import json
import locale
from convertdate import islamic
import requests
from datetime import datetime
import jdatetime
import pytz

def is_user_subscribed(user_id):
    url = f"https://tapi.bale.ai/bot{TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url).json()

    # بررسی وضعیت عضویت
    if "result" in response and response["result"].get("status") in ["member", "administrator", "creator"]:
        return True
    return False

#AI-MEMORI
def chat_with_ai_api(query, user_id):
    try:
        url = "https://api.binjie.fun/api/generateStream"
        headers = {
            "authority": "api.binjie.fun",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://chat18.aichatos.xyz",
            "referer": "https://chat18.aichatos.xyz/",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": query,
            "userId": str(user_id),
            "network": True,
            "system": "",
            "withoutContext": False,
            "stream": False
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        # اگر نیاز به دیکد کردن UTF-8 دارید، می‌توانید از این خط استفاده کنید:
        response.encoding = 'utf-8'
        
        # دریافت محتوای پاسخ به صورت متن
        response_text = response.text

        return f"🤖 **پاسخ هوش مصنوعی** 🤖\n" \
               f"-----------------------------------\n" \
               f"💬 **ورودی شما:** {query}\n" \
               f"📝 **پاسخ:** {response_text}\n" \
               f"-----------------------------------\n" \
               f"✅ تمامی چت های شما با هوش مصنوعی ذخیره می شود!"

    except requests.exceptions.Timeout:
        return "⏳ زمان انتظار به پایان رسید. لطفاً دوباره تلاش کنید."
    except requests.exceptions.RequestException as e:
        return f"🚫 خطا در اتصال به سرور: {str(e)}"
    except Exception as e:
        return f"⚠️ مشکلی رخ داده است: {str(e)}"
    #AI-MOMEN
def chat_with_ai(user_message):
    try:
        response = requests.get(f"https://momen-ai.liara.run/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از دستیار مومن دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور هوش مصنوعی رخ داد."
    #AI-VAKIL
def chat_with_lawyer(user_message):
    try:
        response = requests.get(f"https://vakil-api.liara.run/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از وکیل دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور وکیل رخ داد."
    #AI-RAVAN
def chat_with_psychologist(user_message):
    try:
        response = requests.get(f"https://ravan-api.liara.run/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از روانشناس دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور روانشناسی رخ داد."
    #AI-GPT
def get_gpt(user_message):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/ChatGPT-4o?q={user_message}")
        data = response.json()
        return data.get("results", "پاسخی از ChatGPT دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور ChatGPT رخ داد."
    #TRANS
def get_translate(text):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/GoogleTranslate?text={text}&to=fa")
        data = response.json()
        return data.get("results", "ترجمه‌ای پیدا نشد.")
    except:
        return "مشکلی در ترجمه رخ داد."
#============================================================================================EHSAN-AI==================================================================================================
#============================================================================================EHSAN-TOOLS===============================================================================================
#TIME
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

    days = {
        "Saturday": "شنبه",
        "Sunday": "یکشنبه",
        "Monday": "دوشنبه",
        "Tuesday": "سه‌شنبه",
        "Wednesday": "چهارشنبه",
        "Thursday": "پنج‌شنبه",
        "Friday": "جمعه"
    }

    months = {
        "Farvardin": "فروردین",
        "Ordibehesht": "اردیبهشت",
        "Khordad": "خرداد",
        "Tir": "تیر",
        "Mordad": "مرداد",
        "Shahrivar": "شهریور",
        "Mehr": "مهر",
        "Aban": "آبان",
        "Azar": "آذر",
        "Dey": "دی",
        "Bahman": "بهمن",
        "Esfand": "اسفند"
    }

    today_event = get_today_event(jalali_date)

    return {
        "shamsi_date": jalali_date.strftime("%Y/%m/%d"),
        "gregorian_date": now.strftime("%Y-%m-%d"),
        "hijri_date": hijri_date_str,
        "time": now.strftime("%H:%M:%S"),
        "day": days[jalali_date.strftime("%A")],
        "month": months[jalali_date.strftime("%B")],
        "year": jalali_date.year,
        "remaining_days": remaining_days,
        "event": today_event
    }
    #Shary
def get_prayer_times(city, country="Iran"):
    try:
        url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "data" in data:
            timings = data["data"]["timings"]
            hijri = data["data"]["date"]["hijri"]
            gregorian = data["data"]["date"]["gregorian"]
            meta = data["data"]["meta"]

            # تبدیل نام ماه قمری به فارسی
            english_to_persian = {
                "Muharram": "محرم",
                "Safar": "صفر",
                "Rabi al-Awwal": "ربیع‌الاول",
                "Rabi al-Thani": "ربیع‌الثانی",
                "Jumada al-Awwal": "جمادی‌الاول",
                "Jumada al-Thani": "جمادی‌الثانی",
                "Rajab": "رجب",
                "Sha'ban": "شعبان",
                "Ramadan": "رمضان",
                "Shawwal": "شوال",
                "Dhul-Qadah": "ذی‌القعده",
                "Dhul-Hijjah": "ذی‌الحجه",
            }
            hijri_month_fa = english_to_persian.get(hijri["month"]["en"], hijri["month"]["en"])

            prayer_report = (
                f"🕌 **اوقات شرعی {city}, {country}** 🕌\n\n"
                f"📅 **تاریخ:** {gregorian['date']} ({hijri['date']} هجری قمری)\n"
                f"🌙 **ماه قمری:** {hijri_month_fa}\n"
                f"📍 **موقعیت:** {meta['latitude']}, {meta['longitude']} ({meta['timezone']})\n\n"
                f"🌅 **اذان صبح:** {timings['Fajr']}\n"
                f"☀️ **طلوع آفتاب:** {timings['Sunrise']}\n"
                f"🕌 **اذان ظهر:** {timings['Dhuhr']}\n"
                f"🕒 **اذان عصر:** {timings['Asr']}\n"
                f"🌇 **غروب آفتاب:** {timings['Sunset']}\n"
                f"🕌 **اذان مغرب:** {timings['Maghrib']}\n"
                f"🌙 **اذان عشا:** {timings['Isha']}\n"
                f"🕛 **نیمه‌شب شرعی:** {timings['Midnight']}\n"
                f"🕌 **وقت سحر (امساک):** {timings['Imsak']}\n"
            )
            return prayer_report
        else:
            return "❌ متاسفانه نتوانستم اطلاعات اوقات شرعی را دریافت کنم. لطفاً نام شهر را بررسی کنید."
    except Exception as e:
        return f"⚠️ خطا در دریافت اطلاعات: {str(e)}"
    #font
def convert_to_fonts(text):
    """تبدیل متن به فونت‌های مختلف با استفاده از API"""
    font_url = "https://api.pamickweb.ir/API/FontEn.php?Text="
    
    try:
        # ارسال درخواست به API برای دریافت فونت‌ها
        response = requests.get(font_url + text, timeout=5)
        response.raise_for_status()  # بررسی وضعیت پاسخ سرور
        
        if response.status_code == 200:
            fonts = response.text.split("\n")  # دریافت فونت‌ها و جدا کردن هر فونت در یک خط
            return "\n".join([f"`{font}`" for font in fonts])  # نمایش فونت‌ها به صورت قابل کپی کردن
            
        else:
            return "❌ خطا: نتواستم فونت‌ها را دریافت کنم."
    
    except requests.exceptions.Timeout:
        return "⏳ سرور پاسخگو نیست، لطفاً بعداً امتحان کنید."
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ خطای اتصال: {e}"
    #BRADAY
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

    # محاسبه تعداد روزهای گذشته از تولد
    days_since_birth = (today - birthdate).days  # تعداد روزهای گذشته از تولد

    # محاسبه تعداد روزهای باقی‌مانده تا تولد بعدی
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

    # محاسبه عدد شمع تولد (یک واحد بیشتر از سن)
    birth_number = age + 1

    # محاسبه حیوان سال تولد با ایموجی
    chinese_zodiac_animals = [
        ('موش', '🐭'), ('گاو', '🐂'), ('ببر', '🐅'), ('خرگوش', '🐇'),
        ('اژدها', '🐉'), ('مار', '🐍'), ('اسب', '🐎'), ('بز', '🐐'),
        ('میمون', '🐒'), ('مرغ', '🐔'), ('سگ', '🐕'), ('خوک', '🐖')
    ]
    zodiac_animal, zodiac_emoji = chinese_zodiac_animals[birthdate.year % 12]

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

🐀 **حیوان سال تولد شما:** {zodiac_animal} {zodiac_emoji}
"""
    return result
    #GOLD
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
    #WHATER
def get_weather(city):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/Weather?city={city}")
        data = response.json()

        if data['status']:  # بررسی وضعیت پاسخ API
            current = data['results']['current']
            weather_report = (
                f"🌀 وضعیت آب و هوا در {city} 🌀\n\n"
                f"🌡️ دما: {current['temperature']['value']} °C\n"
                f"🌥️ وضعیت هوا: {current['weather']['value']}\n"
                f"💨 سرعت باد: {current['windspeed']['value']} km/h\n"
                f"🌬️ جهت باد: {current['wind_direction']['value']}\n"
                f"💧 رطوبت هوا: {current['humidity']['value']}%\n"
                f"⚖️ فشار جو: {current['pressure']['value']} mb\n"
                f"☁️ پوشش ابر: {current['cloudcover']['value']}%\n"
                f"🌫️ دید: {current['visibility']['value']} km\n"
                f"🥶 دمای احساس‌شده: {current['feels_like']['value']} °C\n"
                f"🌧️ میزان بارش: {current['precipitation']['value']} mm\n"
                f"🌞 شاخص UV: {current['uv_index']['value']}\n"
                f"🌅 زمان طلوع آفتاب: {current['sunrise']['value']}\n"
                f"🌇 زمان غروب آفتاب: {current['sunset']['value']}\n"
                f"🌙 زمان طلوع ماه: {current['moonrise']['value']}\n"
                f"🌘 زمان غروب ماه: {current['moonset']['value']}\n"
                f"📅 آخرین بروزرسانی: {current['last_updated']['value']}\n\n"
                f"🕰️ پیش‌بینی ساعتی:\n"
                f"🔹 00:00 | دما: {data['results']['hourly_forecast'][0]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][0]['weather']}\n"
                f"🔹 03:00 | دما: {data['results']['hourly_forecast'][1]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][1]['weather']}\n"
                f"🔹 06:00 | دما: {data['results']['hourly_forecast'][2]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][2]['weather']}\n"
                f"🔹 09:00 | دما: {data['results']['hourly_forecast'][3]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][3]['weather']}\n"
                f"🔹 12:00 | دما: {data['results']['hourly_forecast'][4]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][4]['weather']}\n"
                f"🔹 15:00 | دما: {data['results']['hourly_forecast'][5]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][5]['weather']}\n"
                f"🔹 18:00 | دما: {data['results']['hourly_forecast'][6]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][6]['weather']}\n"
                f"🔹 21:00 | دما: {data['results']['hourly_forecast'][7]['temperature']} °C | وضعیت: {data['results']['hourly_forecast'][7]['weather']}\n"
            )
            return weather_report
        else:
            return "متاسفانه نتواستم اطلاعات آب و هوا را پیدا کنم. لطفاً نام شهر را بررسی کنید."
    except Exception as e:
        return f"خطا در دریافت اطلاعات: {str(e)}"
    #FOTBAL
def get_fot():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/Footballi", timeout=10)
        response.raise_for_status()  # بررسی وضعیت پاسخ (۴xx یا ۵xx)
        data = response.json()

        if not data.get('status', False):
            return "متاسفانه نتوانستم اطلاعات بازی‌های امروز را دریافت کنم."

        matches = data.get('results', [])
        if not matches:
            return "اطلاعات بازی‌ها در دسترس نیست."

        match_report = "⚽ بازی‌های امروز:\n\n"
        
        for match in matches[:20]:  # محدود کردن به ۲۰ بازی اول
            competition = match.get('competition', 'نامشخص') or 'نامشخص'
            home_team = match.get('home_team', 'نامشخص') or 'نامشخص'
            away_team = match.get('away_team', 'نامشخص') or 'نامشخص'
            time = match.get('time', 'زمان مشخص نیست') if match.get('time') and match.get('time') != "N/A" else "زمان مشخص نیست"
            url = match.get('url', '')

            match_report += (
                f"🏆 {competition}\n"
                f"🏠 {home_team} vs {away_team}\n"
                f"⏰ زمان: {time}\n"
                f"🔗 {'[مشاهده بازی](' + url + ')' if url else 'لینک موجود نیست'}\n\n"
            )

        return match_report

    except requests.exceptions.RequestException as req_err:
        return f"خطا در اتصال به سرور: {req_err}"
    except Exception as e:
        return f"خطا در پردازش اطلاعات بازی‌ها: {e}"
    #TIPAX
def track_parcel(tracking_code):
    # بررسی اینکه آیا کد رهگیری 21 رقمی است
    if len(tracking_code) != 21 or not tracking_code.isdigit():
        return "❌ کد رهگیری باید ۲۱ رقمی و عددی باشد."

    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/TipaxInfo?code={tracking_code}")
        
        # بررسی وضعیت پاسخ HTTP
        if response.status_code != 200:
            return "❌ خطا در اتصال به سرور."
        
        data = response.json()

        # بررسی اینکه آیا اطلاعات معتبر برگشت داده شده است
        if not data.get("status", False):
            return "🔮اطلاعات مرسوله پیدا نشد."
        
        results = data.get("results", {})
        if not results:
            return "🔮اطلاعات مرسوله پیدا نشد."

        sender = results.get("sender", {})
        receiver = results.get("receiver", {})
        status_info = results.get("status_info", [])

        # ساخت پیام کامل با اطلاعات بیشتر
        parcel_info = f"📤فرستنده: {sender.get('name', 'نامشخص')} از {sender.get('city', 'نامشخص')}\n"
        parcel_info += f"🏢تعداد ارسال‌ها: {results.get('dispatch_count', 'نامشخص')}\n"
        parcel_info += f"💰هزینه پست: {results.get('package_cost', 'نامشخص')} تومان\n"
        parcel_info += f"📦نوع بسته: {results.get('COD', 'نامشخص')}\n"
        parcel_info += f"🚚وزن: {results.get('weight', 'نامشخص')} کیلوگرم\n"
        parcel_info += f"💸هزینه کل: {results.get('total_cost', 'نامشخص')} تومان\n"
        parcel_info += f"🔄وضعیت پرداخت: {results.get('pay_type', 'نامشخص')}\n"
        parcel_info += f"🌍مسافت: {results.get('city_distance', 'نامشخص')} کیلومتر\n"
        parcel_info += f"📍زون: {results.get('distance_zone', 'نامشخص')}\n"
        
        parcel_info += f"\n📥گیرنده: {receiver.get('name', 'نامشخص')} در {receiver.get('city', 'نامشخص')}\n"
        
        if status_info:
            for status in status_info:
                parcel_info += f"\n📝تاریخ: {status.get('date', 'نامشخص')}\n"
                parcel_info += f"🔹وضعیت: {status.get('status', 'نامشخص')}\n"
                parcel_info += f"📍محل: {status.get('representation', 'نامشخص')}\n"
        else:
            parcel_info += "\n🔮وضعیت مرسوله موجود نیست."

        return parcel_info

    except Exception as e:
        return f"❌ خطا: {str(e)}"
    #MOBILE
def mobile(mo):
    try:
        url = f"https://open.wiki-api.ir/apis-1/MobileSearch?q={mo}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status', False):
                mobiles = data.get('results', [])
                if mobiles:
                    result = "📱 نتایج جستجوی شما:\n\n"
                    for mobile in mobiles:
                        name = mobile.get('name', 'نامشخص')
                        image = mobile.get('image', 'ندارد')
                        link = mobile.get('url', '#')
                        
                        result += (f"🔍 نام: {name}\n"
                                   f"🔗 [مشاهده مشخصات]({link})\n\n")
                    return result
                else:
                    return "😔 هیچ نتیجه‌ای پیدا نشد."
            else:
                return "⚠️ مشکلی در دریافت اطلاعات از API وجود دارد. لطفاً دوباره تلاش کنید."
        else:
            return f"😓 خطای HTTP: {response.status_code}"
    
    except requests.exceptions.Timeout:
        return "⏳ زمان انتظار به پایان رسید. لطفاً دوباره تلاش کنید."
    except requests.exceptions.RequestException as e:
        return f"❌ خطا در اتصال: {e}"
    except Exception as e:
        return "❌ مشکلی رخ داده است. لطفاً دوباره تلاش کنید."
    #APARAT
def aparat(query):
    try:
        url = f"https://open.wiki-api.ir/apis-1/AparatSearch?q={query}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status", False):
                videos = data.get("results", [])
                
                if videos:
                    result = "🎥 نتایج جستجو در آپارات:\n\n"
                    for video in videos[:5]:  # نمایش 5 نتیجه اول
                        title = video.get("title", "بدون عنوان")
                        link = video.get("frame", "#")
                        poster = video.get("small_poster", "")
                        visits = video.get("visit_cnt", 0)

                        result += (f"📌 عنوان: {title}\n"
                                   f"👁️ بازدید: {visits}\n"
                                   f"🔗 [مشاهده ویدیو]({link})\n\n")
                    return result
                else:
                    return "😔 هیچ ویدیویی مرتبط پیدا نشد."
            else:
                return "⚠️ مشکلی در دریافت اطلاعات از API وجود دارد."
        else:
            return f"❌ خطای HTTP: {response.status_code}"
    
    except requests.exceptions.Timeout:
        return "⏳ زمان انتظار به پایان رسید. لطفاً دوباره تلاش کنید."
    except requests.exceptions.RequestException as e:
        return f"❌ خطا در اتصال به سرور: {e}"
    except Exception:
        return "🚫 مشکلی رخ داده است. لطفاً دوباره تلاش کنید."
    #KALA
def digikala(query):
    try:
        url = f"https://open.wiki-api.ir/apis-1/SearchDigikala?q={query}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            
            if data.get("status", False):
                products = data.get("results", [])
                
                if products:
                    result = "**🛒 نتایج جستجو در دیجی‌کالا:\n\n**"
                    for item in products[:5]:  # نمایش 5 نتیجه اول
                        product = item.get("product", {})
                        title = product.get("title_fa", "بدون عنوان")
                        price = product.get("price", 0)
                        image = product.get("image", [""])[0]
                        link = product.get("url", "#")
                        seller = item.get("seller", {}).get("name", "نامشخص")

                        result += (f"📌 نام محصول: {title}\n"
                                   f"💰 قیمت: {price:,} تومان\n"
                                   f"🛍️ فروشنده: {seller}\n"
                                   f"🔗 [مشاهده محصول]({link})\n\n")
                    return result
                else:
                    return "😔 هیچ محصولی مرتبط پیدا نشد."
            else:
                return "⚠️ مشکلی در دریافت اطلاعات از API وجود دارد."
        else:
            return f"❌ خطای HTTP: {response.status_code}"
    
    except requests.exceptions.Timeout:
        return "⏳ زمان انتظار به پایان رسید. لطفاً دوباره تلاش کنید."
    except requests.exceptions.RequestException as e:
        return f"❌ خطا در اتصال به سرور: {e}"
    except Exception:
        return "🚫 مشکلی رخ داده است. لطفاً دوباره تلاش کنید."
    #MUSIC
def music(query):
    try:
        url = f"https://open.wiki-api.ir/apis-1/SearchAhangify?q={query}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("status", False):
                artists = data.get("results", {}).get("artists", [])
                
                if artists:
                    result = "🎶✨ **نتایج جستجو آهنگ** ✨🎶\n"
                    result += "-----------------------------------\n"
                    for artist in artists[:5]:  # فقط 5 نتیجه اول
                        name = artist.get("name", "نامشخص")
                        cover = artist.get("cover", "")
                        artist_id = artist.get("id", "")
                        link = f"https://ahangify.com/artist/{artist_id}" if artist_id else "#"

                        result += f"🔥 **نام خواننده:** {name}\n"
                        if cover:
                            result += f"🔗 [مشاهده پروفایل]({link})\n"
                        result += "-----------------------------------\n"

                    result += "✅ برای دریافت اطلاعات بیشتر روی لینک‌ها کلیک کنید."
                    return result
                else:
                    return "😔 هیچ خواننده‌ای مرتبط پیدا نشد. لطفاً دوباره امتحان کنید."
            else:
                return "⚠️ خطا در دریافت اطلاعات از سرور. لطفاً بعداً تلاش کنید."
        else:
            return f"❌ خطای HTTP: {response.status_code}"

    except requests.exceptions.Timeout:
        return "⏳ زمان انتظار به پایان رسید. لطفاً دوباره تلاش کنید."
    except requests.exceptions.RequestException:
        return "🚫 خطا در اتصال به سرور. لطفاً بعداً تلاش کنید."
    except Exception:
        return "⚠️ مشکلی رخ داده است. لطفاً دوباره امتحان کنید."
#============================================================================================EHSAN-TOOLS===============================================================================================
#============================================================================================EHSAN-FUN=================================================================================================
    #hadith
def get_hadith():
    try:
        response = requests.get("https://hadis-api.liara.run/random_hadith")
        data = response.json()
        return data.get("hadith", "حدیثی پیدا نشد."), data.get("speaker", "نام سخنران پیدا نشد.")
    except:
        return "مشکلی در دریافت حدیث رخ داد.", "نامشخص"
    #JOKE
def get_joke():
    try:
        response = requests.get("https://open.wiki-api.ir/apis-1/4Jok")
        data = response.json()
        return f"😂 {data['results']['post']}"
    except:
        return "مشکلی در دریافت جوک رخ داد."
    #FACT
def get_fact():
    try:
        response = requests.get("https://fact-api.onrender.com/f")
        data = response.json()
        return data.get("fact", "دانستی پیدا نشد."), data.get("source", "منبع پیدا نشد.")
    except:
        return "مشکلی در دریافت دانستنی رخ داد.", "نامشخص"
    #BOZORGAN
def get_wise_quote():
    """دریافت نقل قول از API حرف بزرگان با افکت‌های متنی"""
    url = "https://api.pamickweb.ir/API/bozorg.php"
    try:
        response = requests.get(url, timeout=5)  # اضافه کردن Timeout
        response.raise_for_status()  # بررسی وضعیت HTTP
        quote = response.text.strip()  # حذف فاصله‌های اضافی از متن
        
        # 🎨 افکت برای نمایش زیباتر نقل قول
        formatted_quote = f"""
📜 **حرف بزرگان:**
━━━━━━━━━━━━━━━
❝ {quote} ❞
━━━━━━━━━━━━━━━
💡 الهام بگیر و ادامه بده!
"""
        return formatted_quote

    except requests.exceptions.Timeout:
        return "⏳ سرور پاسخگو نیست، لطفاً بعداً امتحان کنید."
    except requests.exceptions.RequestException as e:
        return f"⚠️ خطای اتصال: {e}"
    #ZEKR
def get_zekr():
    """دریافت ذکر هفته از API"""
    url = "https://api.pamickweb.ir/API/zekr.php"
    
    try:
        response = requests.get(url, timeout=5)  # تنظیم Timeout
        response.raise_for_status()  # بررسی وضعیت پاسخ سرور
        
        if response.status_code == 200:
            data = response.json()  # تبدیل پاسخ به فرمت JSON
            
            if data.get("ok"):
                zekr = data["Result"]["zekr"]
                persian = data["Result"]["persian"]
                info = data["Result"]["info"]
                
                # خروجی مرتب و خوانا
                output = (
                    f"✨ **ذکر هفته:** {zekr} ✨\n\n"
                    f"🌸 {persian} 🌸\n\n"
                    f"💬 **توضیحات:** {info}"
                )
                
                return output
            else:
                return "❌ **خطا:** مشکلی در دریافت ذکر هفته به وجود آمده است."
        else:
            return "❌ **خطا:** پاسخ سرور صحیح نیست. لطفاً دوباره تلاش کنید."
    except requests.exceptions.RequestException:
        return "❌ **خطا:** اتصال به سرور برقرار نشد. لطفاً اینترنت خود را بررسی کنید."
    except requests.exceptions.RequestException as e:
        return f"⚠️ <b>خطای اتصال:</b> {e}"
