import telebot
from telebot import types
import datetime

# إعدادات البوت
API_TOKEN = '7672935277:AAH0Z0N58y8zB7vY_M9k_uN_m5_h5_h5'
bot = telebot.TeleBot(API_TOKEN)

# 🛡️ إعدادات الإدارة (إبراهيم فقط)
MY_ADMIN_ID = 7155512786
ADMIN_PASSWORD = "Haker99"

# 📂 قاعدة بيانات المستخدمين {ID: تاريخ الانتهاء}
authorized_users = {} 

@bot.message_handler(func=lambda message: True)
def master_controller(message):
    user_id = message.from_user.id

    # 1. لوحة تحكم إبراهيم (الآدمن)
    if user_id == MY_ADMIN_ID:
        if message.text == ADMIN_PASSWORD:
            show_main_menu(message)
        elif message.text == "➕ تفعيل مستخدم جديد":
            msg = bot.send_message(message.chat.id, "أرسل الـ ID الخاص بالمستخدم الجديد:")
            bot.register_next_step_handler(msg, get_new_user_id)
        elif message.text == "🚫 إيقاف مستخدم":
            msg = bot.send_message(message.chat.id, "أرسل الـ ID الذي تريد إيقافه:")
            bot.register_next_step_handler(msg, revoke_user)
        elif message.text == "👥 عرض المشتركين":
            show_subscribers(message)
        # (باقي الأزرار القديمة تعمل هنا أيضاً)
        return

    # 2. نظام التحقق للمستخدمين الآخرين
    if user_id in authorized_users:
        if datetime.datetime.now() < authorized_users[user_id]:
            if message.text == "/start":
                bot.reply_to(message, "✅ اشتراكك فعال. يمكنك استخدام البوت الآن.")
        else:
            bot.reply_to(message, "❌ انتهت مدة اشتراكك. تواصل مع المطور للتجديد.")
    else:
        # صمت تام للغرباء
        pass

# --- وظائف الإدارة ---

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("➕ تفعيل مستخدم جديد", "🚫 إيقاف مستخدم", "👥 عرض المشتركين", "🤖 ذكاء اصطناعي", "📱 تحويل الكود لتطبيق")
    bot.send_message(message.chat.id, "👑 لوحة تحكم القائد إبراهيم جاهزة:", reply_markup=markup)

def get_new_user_id(message):
    try:
        new_id = int(message.text)
        msg = bot.send_message(message.chat.id, "كم عدد أيام التفعيل؟")
        bot.register_next_step_handler(msg, lambda m: finalize_user(m, new_id))
    except:
        bot.reply_to(message, "❌ خطأ! أرسل رقماً صحيحاً.")

def finalize_user(message, new_id):
    try:
        days = int(message.text)
        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        authorized_users[new_id] = expiry
        bot.send_message(message.chat.id, f"✅ تم تفعيل المستخدم {new_id} لمدة {days} يوم.")
    except:
        bot.reply_to(message, "❌ خطأ في إدخال الأيام.")

def revoke_user(message):
    try:
        target_id = int(message.text)
        if target_id in authorized_users:
            del authorized_users[target_id]
            bot.send_message(message.chat.id, f"🚫 تم حظر المستخدم {target_id} بنجاح.")
        else:
            bot.reply_to(message, "⚠️ هذا المستخدم غير موجود في القائمة.")
    except:
        bot.reply_to(message, "❌ خطأ في الإدخال.")

def show_subscribers(message):
    if not authorized_users:
        bot.send_message(message.chat.id, "📭 لا يوجد مشتركين حالياً.")
        return
    text = "📊 قائمة المشتركين:\n"
    for uid, date in authorized_users.items():
        text += f"\n👤 {uid} - ينتهي: {date.strftime('%Y-%m-%d')}"
    bot.send_message(message.chat.id, text)

bot.infinity_polling()
