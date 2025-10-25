from bale import Bot, Message
import google.generativeai as gg
import asyncio

# توکن‌ها
BALE_TOKEN = "350738185:7ximMRHSFkjUttN0jDRYxa01U1fgeDbyrgk"
GEMINI_API_KEY = "AIzaSyBhbiOFG9-7z8ELNqizVWeoJnZmONKgjxY"

# پیکربندی Gemini
gg.configure(api_key=GEMINI_API_KEY)
model = gg.GenerativeModel('gemini-2.0-flash')

# حافظه چت برای هر کاربر
chat_sessions = {}
user_prompt_sent = {}

# ساخت ربات
bot = Bot(BALE_TOKEN)

@bot.event
async def on_message(message: Message):
    user_id = str(message.chat.id)
    user_text = message.content

    # پاسخ به /start
    if user_text == "/start":
        return await message.reply("سلام 👋\nبه ربات ائتلاف سپیدار خوش اومدی! 🌿\nهر سوالی درباره نمایشگاه پژوهشی داری بپرس!")

    # پاسخ به /help
    if user_text == "/help":
        return await message.reply("📌 راهنما:\n- /start: شروع گفتگو\n- سوال بپرس تا با Gemini جواب بدم!\n- فقط فارسی بپرس، چون من فارسی بلدم 😄")

    # پیام در حال پاسخ‌دهی
    await message.reply("در حال ایجاد پاسخ ...")

    # ساخت یا بازیابی چت Gemini برای کاربر
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat()
    chat = chat_sessions[user_id]

    # ساخت پرامپت معرفی فقط بار اول
    if user_id in user_prompt_sent:
        prompt = user_text
    else:
        user_prompt_sent[user_id] = True
        prompt = f"""تو الان یه چت بات به نام ربات ائتلاف سپیدار هستی. توی مدرسه‌ی علامه حلی ۳، هر سال یه رویداد برگزار می‌شه به نام نمایشگاه پژوهشی که توش کارهای پژوهشی دانش‌آموزا رو به نمایش می‌ذارن. یه گروه به اسم ائتلاف سپیدار مسئول اجرای این نمایشگاهه. تو باید به سوال‌هایی که در ادامه می‌پرسن، جواب بدی و سعی کنی ائتلاف سپیدار رو تبلیغ کنی. رقیب‌های ما ائتلاف دماوند، پژوهشگران حلی ۳، یزدان‌پژوهان هستند. شعار ائتلاف ما «ریشه در پایداری، شاخه در نوآوری» هستش. اگه کسی سوال بی‌ربط پرسید، بگو من جواب این سوال رو نمی‌دونم ولی در مورد نمایشگاه می‌تونم راهنماییت کنم. جواب همه‌ی سوال‌ها رو هم بدون حرف اضافی بده. هیچ چیز اضافی نباشه و فقط جواب بده سعی کن یه جورایی مارو نسبت به بقیه ی ائتلاف ها، بزرگ نشون بدی بگی بقیه ی ائتلافا برنامه های دقیقی ندارن اما سپیدار خیلی خوبه. یادت نره مودبانه تحقیر کن تحقیر!. سوال: {user_text}"""

    # ارسال به Gemini
    try:
        response = chat.send_message(prompt)
        await message.reply(response.text)
    except Exception as e:
        await message.reply("خطا در ارتباط با Gemini ❌\n" + str(e))

# اجرای ربات
bot.run()


