import os
import telebot
from yt_dlp import YoutubeDL

# ضع الرمز (Token) الذي أعطاك إياه BotFather هنا بين علامتي التنصيص
TOKEN = "9153815856:AAFoArQY7851LnwZ_0AtkjP-ZplYuWC55gU"
bot = telebot.TeleBot(TOKEN)

# رسالة الترحيب عند الضغط على Start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في Velvet Bot 🖤\nأرسل لي أي رابط فيديو (يوتيوب، تيك توك، إنستجرام) وسأقوم بتحميله لك فوراً.")

# استقبال الروابط وتحميلها
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "يرجى إرسال رابط صحيح يبدأ بـ http أو https")
        return

    msg = bot.reply_to(message, "⏳ جاري معالجة وتحميل الفيديو، قليلاً من الدلال...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024, # تحديد الحجم لكي يناسب التليجرام مؤقتاً
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو للمستخدم
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة Velvet Bot 🖤")

        # حذف الملف من الجهاز بعد الإرسال لتوفير المساحة
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء التحميل: تأكد من صحة الرابط أو أن حجم الفيديو ضمن المسموح.\nالتفاصيل: {str(e)}", message.chat.id, msg.message_id)

print("Bot is running...")
bot.infinity_polling()

