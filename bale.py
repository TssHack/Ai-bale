import json
import locale
from convertdate import islamic
from balethon import Client
from balethon.objects import InlineKeyboard, ReplyKeyboard
from balethon.conditions import is_joined
import requests
from datetime import datetime
import jdatetime
import pytz

# تنظیمات ربات
bot_token = "‏‏1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO"
CHANNEL_ID = "@sartaaa"
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

# تابع دریافت حدیث
def get_hadith():
    try:
        response = requests.get("https://hadis-api.liara.run/random_hadith")
        data = response.json()
        return data.get("hadith", "حدیثی پیدا نشد."), data.get("speaker", "نام سخنران پیدا نشد.")
    except:
        return "مشکلی در دریافت حدیث رخ داد.", "نامشخص"
  

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

#music
def music(query):
    try:
        url = f"https://open.wiki-api.ir/apis-1/SearchAhangify?q={query}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("status", False):
                artists = data.get("results", {}).get("artists", [])
                
                if artists:
                    result = "🎶✨ **نتایج جستجوی نام خواننده** ✨🎶\n"
                    result += "-----------------------------------\n"
                    for artist in artists[:10]:  # فقط 5 نتیجه اول
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
        
#aparst
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
                                   f"💰 قیمت: {price:,} ریال\n"
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

#mobile

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
        
#photo
def photo(query):
    try:
        # ارسال درخواست به API برای ساخت تصویر
        url = f"https://open.wiki-api.ir/apis-1/MakePhotoAi?q={query}"
        response = requests.get(url, timeout=10)
        
        # بررسی وضعیت پاسخ HTTP
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status', False):
                image_url = data['results'].get('img', '')
                if image_url:
                    return f"🎉 تصویر شما با موفقیت ساخته شد! 🎨 برای مشاهده آن روی لینک زیر کلیک کنید: [مشاهده تصویر]({image_url}) 😍"
                else:
                    return "😔 متاسفانه نتواستیم تصویر مورد نظر را بسازیم. لطفاً دوباره تلاش کنید."
            else:
                return "⚠️ خطا در ارتباط با API. لطفاً دوباره تلاش کنید."
        else:
            return "😓 مشکلی در دریافت داده‌ها پیش آمده است. لطفاً دوباره تلاش کنید."
    
    except Exception as e:
        return "❌ خطا در اتصال به سرویس. لطفاً دوباره تلاش کنید."

def get_fact():
    try:
        response = requests.get("https://fact-api.onrender.com/f")
        data = response.json()
        return data.get("fact", "دانستی پیدا نشد."), data.get("source", "منبع پیدا نشد.")
    except:
        return "مشکلی در دریافت دانستنی رخ داد.", "نامشخص"
# city
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

# تابع چت با هوش مصنوعی اسلامی
def chat_with_ai(user_message):
    try:
        response = requests.get(f"https://momen-ai.liara.run/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از دستیار مومن دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور هوش مصنوعی رخ داد."
#gpt
def get_gpt(user_message):
    try:
        response = requests.get(f"https://open.wiki-api.ir/apis-1/ChatGPT-4o?q={user_message}")
        data = response.json()
        return data.get("results", "پاسخی از ChatGPT دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور ChatGPT رخ داد."

# تابع چت با وکیل هوش مصنوعی
def chat_with_lawyer(user_message):
    try:
        response = requests.get(f"https://vakil-api.liara.run/?text={user_message}")
        data = response.json()
        return data.get("message", "پاسخی از وکیل دریافت نشد.")
    except:
        return "مشکلی در ارتباط با سرور وکیل رخ داد."

# تابع چت با روانشناس هوش مصنوعی
def chat_with_psychologist(user_message):
    try:
        response = requests.get(f"https://ravan-api.liara.run/?text={user_message}")
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
        
#فوتبال
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


# تابع پیگیری مرسوله تیپاکسimport requests

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
    
# دکمه‌های اینلاین
inline_buttons = InlineKeyboard(
    [("🤖 بخش هوش مصنوعی", "ai_services")],
    [("📌 بخش کاربردی و ابزاری", "tools")],
    [("🎯 بخش سرگرمی و علمی", "fun_science")],
    [("ℹ️ درباره ما", "info"), ("راهنما 🧬", "help")]
)

tools_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time")],
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
    [("جوک تصادفی 😂", "random_joke"), ("دانستنی 🧠")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

ai_services_buttons = InlineKeyboard(
    [("هوش مصنوعی حافظه دار 🧠", "gpt1")],
    [("دستیار مومن 🤖", "ai_chat")],
    [("وکیل ⚖️", "lawyer"), ("روانشناس 🧠", "psychologist")],
    [("ChatGPT-4o 🧩", "gpt")],
    [("تولید تصویر 🤳", "p")],
    [("مترجم انگلیسی 📝", "translate")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])
join = InlineKeyboard([InlineButton("🔗 عضویت در کانال", url="https://t.me/your_channel")])
Ai_back = InlineKeyboard([("🔙", "Ai_b")])

@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if not is_joined(CHANNEL_ID)(message):  # بررسی عضویت در کانال
        await message.reply("🚫 برای استفاده از ربات، ابتدا در کانال ما عضو شوید.", reply_markup=join)
        return  # از اینجا دیگر هیچ‌کدام از دستورات بعدی اجرا نمی‌شوند

    if state is None:
        await message.reply("🤖 به ربات صراط خوش آمدید!\n\n✨ دستیار هوشمند اسلامی شما ✨\n\n📌 این ربات امکانات متنوعی را در اختیار شما قرار می‌دهد:", reply_markup=return_to_main_menu_button)
    else:
        await message.reply("✅ شما عضو کانال هستید! از ربات استفاده کنید.", reply_markup=return_to_main_menu_button)
    elif state == "tracking":
        tracking_code = message.text.strip()
        response = track_parcel(tracking_code)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None 

    elif state == "get_weather":
        city = message.text.strip()
        response = get_weather(city)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None  

    elif state == "s-m":
        mo = message.text.strip()
        response = mobile(mo)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "s-a":
        query = message.text.strip()
        response = aparat(query)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "s-mu":
        query = message.text.strip()
        response = music(query)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "s-d":
        query = message.text.strip()
        response = digikala(query)
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None

    elif state == "photo-ai":
        query = message.text.strip()
        response = photo(query)
        await message.reply(response, reply_markup=ai_services_buttons)
        user_states[chat_id] = None  

    elif state == "get_translate":
        translation = get_translate(message.text)
        await message.reply(f"📜 **متن ترجمه‌شده:**\n{translation}", reply_markup=ai_services_buttons)
        user_states[chat_id] = None  

    elif state == "get_birthdate":
        response = calculate_age(message.text.strip())
        await message.reply(response, reply_markup=tools_buttons)
        user_states[chat_id] = None  

    elif state == "ai_chat":
        response = chat_with_ai(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state == "gpt-1":
        user_id = message.chat.id  # شناسه کاربر را از پیام دریافت می‌کنید
        query = message.text
        response = chat_with_ai_api(query, user_id)  # ارسال پیام کاربر و شناسه به تابع
        await message.reply(response, reply_markup=Ai_back)

    elif state == "gpt-chat":
        response = get_gpt(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state == "lawyer":
        response = chat_with_lawyer(message.text)
        await message.reply(response, reply_markup=Ai_back)

    elif state == "psychologist":
        response = chat_with_psychologist(message.text)
        await message.reply(response, reply_markup=Ai_back)

    if state not in ["ai_chat", "lawyer", "psychologist", "gpt-chat", "gpt-1"]:
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

    elif callback_query.data == "hadith":
        hadith, speaker = get_hadith()
        await callback_query.message.edit_text(f"📖 **حدیث:**\n{hadith}\n🗣️ **{speaker}**", reply_markup=tools_buttons)

    elif callback_query.data == "facts":
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

    elif callback_query.data == "p":
        user_states[chat_id] = "photo-ai"
        await callback_query.message.edit_text("🔮 **موضوع یا هر چیزی که می خواهید تصویر آن را بسازید را به صورت انگلیسی ارسال کنید :**")

    elif callback_query.data == "Ai_b":
        user_states[chat_id] = None
        await callback_query.message.edit_text("👀به بخش هوش مصنوعی برگشتید", reply_markup= ai_services_buttons)
# اجرای ربات
bot.run()
