# bot.py - Irbah Cash DZ 💰🇩🇿
import telebot
from telebot import types
import sqlite3
import time
from datetime import datetime

user_states = {}
withdraw_data = {}
API_TOKEN = "8061542154:AAGBY8d9TUa0JOwPKuARnWPeAY_QGGRidgU"  # ← غيّرها بالتوكن تاعك
ADMIN_ID = 6643841792
bot = telebot.TeleBot(API_TOKEN)

# 🧠 دالة عرض القائمة الرئيسية حسب نوع المستخدم (أدمن أو مشترك عادي)
def send_main_menu(user_id, text="✅ تم الرجوع إلى القائمة الرئيسية."):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💼 التسجيل", "💸 دفع الاشتراك")
    markup.row("📊 أرباحي", "🧮 نقاطي")
    markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
    markup.row("ℹ️ معلومات")
    if user_id == ADMIN_ID:
        markup.row("⚙️ لوحة التحكم")
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="HTML")
# === قاعدة البيانات ===
def init_db():
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        referrer_id INTEGER,
        referral_points INTEGER DEFAULT 0,
        referral_bonus_count INTEGER DEFAULT 0,
        vip_level TEXT,
        subscribed INTEGER DEFAULT 0,
        vip_start_date TEXT,
        last_payout TEXT,
        balance INTEGER DEFAULT 0,
        last_withdraw_date TEXT,
        pending_vip_level TEXT,
        payment_method TEXT,
        payment_pending INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()
# === رسالة /start ===
import telebot
from telebot import types
import sqlite3

# ✅ عرّف توكن البوت تاعك هنا
API_TOKEN = "8061542154:AAGBY8d9TUa0JOwPKuARnWPeAY_QGGRidgU"
bot = telebot.TeleBot(API_TOKEN)

# ✅ عرّف معرف الأدمن (Aymen Kasmi)
ADMIN_ID = 6643841792
# 🟢 انسخه وضعه بعد سطر ADMIN_ID مباشرة
def send_main_menu(user_id, text="✅ تم الرجوع إلى القائمة الرئيسية."):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💼 التسجيل", "💸 دفع الاشتراك")
    markup.row("📊 أرباحي", "🧮 نقاطي")
    markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
    markup.row("ℹ️ معلومات")
    if user_id == ADMIN_ID:
        markup.row("⚙️ لوحة التحكم")
    bot.send_message(user_id, text, reply_markup=markup)

    return markup
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "بدون"
    first_name = message.from_user.first_name or "مستخدم"

    # إضافة المستخدم إلى قاعدة البيانات إن لم يكن موجود
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_exists = cur.fetchone()

    referrer_id = None
    if message.text.startswith("/start ") and not user_exists:
        ref_data = message.text.split()[1]
        if ref_data.isdigit():
            referrer_id = int(ref_data)

    if not user_exists:
        cur.execute("INSERT INTO users (user_id, username, first_name, referrer_id) VALUES (?, ?, ?, ?)",
                    (user_id, username, first_name, referrer_id))
        conn.commit()
    conn.close()

    # توليد رابط الإحالة
    referral_link = f"https://t.me/irbahdzbot?start={user_id}"

    # رسالة ترحيب احترافية
    welcome_text = f"""
<b>👋 أهلاً وسهلاً بك {first_name}!</b>

🔒 <b>Irbah Cash DZ</b> هو مشروع استثماري رقمي 🇩🇿💸 يتيح لك تحقيق دخل شهري مضمون وبطريقة آمنة وشفافة 100%.

<b>🚀 كيف تبدأ؟</b>
• اختر عرض اشتراك VIP يناسبك (مرة واحدة فقط)
• استلم أرباحك الشهرية <b>بشكل تلقائي</b>
• لا تحتاج أي خبرة أو عمل يومي

<b>💰 مثال:</b>
عرض VIP1 بـ 9000 دج يعطيك شهرياً <b>2700 دج مدى الحياة</b> حتى بدون إحالات!

<b>🎁 نظام الإحالة:</b>
• كل شخص يسجل من رابطك = <b>+3 نقاط</b>
• كل 20 نقطة = <b>1.5 USDT هدية</b> 🎉
(يمكنك تجميع العلاوات بدون حد أقصى!)

<b>🔗 رابط إحالتك الشخصي:</b>
<code>{referral_link}</code>

📌 <b>نصيحة:</b> انسخ الرابط وابدأ نشره لأصدقائك الآن، كل شخص تسجلو = تربح أكثر!

⚙️ استعمل الأزرار بالأسفل لاختيار العرض، الدفع، أو سحب أرباحك.
"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💼 التسجيل", "💸 دفع الاشتراك")
    markup.row("📊 أرباحي", "🧮 نقاطي")
    markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
    markup.row("ℹ️ معلومات")

    # زر الأدمن يظهر فقط للأدمن
    if user_id == 6643841792:
        markup.row("⚙️ لوحة الأدمن")

    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode="HTML")


@bot.message_handler(func=lambda msg: msg.text == "⚙️ لوحة التحكم")
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "🚫 هذه الميزة خاصة بالأدمن فقط.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 قائمة المشتركين", "📋 طلبات السحب")
    markup.row("🔙 رجوع")
    bot.send_message(message.chat.id, "📍 لوحة تحكم الأدمن:", reply_markup=markup)
# === التسجيل واختيار العرض ===
@bot.message_handler(func=lambda m: m.text == "💼 التسجيل")
def choose_subscription(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("اشتراك أول", "VIP1")
    markup.row("VIP2", "VIP3")
    markup.row("VIP4", "🔙 رجوع")
    bot.send_message(message.chat.id, "💼 اختر العرض الذي يناسبك:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["اشتراك أول", "VIP1", "VIP2", "VIP3", "VIP4"])
def select_vip_offer(message):
    user_id = message.from_user.id
    offer = message.text
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET pending_vip_level = ?, payment_pending = 0 WHERE user_id = ?", (offer, user_id))
    user_states[user_id] = "registering"
    conn.commit()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("✅ تأكيد التسجيل", "❌ إلغاء")
    bot.send_message(user_id, f"🔘 لقد اخترت العرض: <b>{offer}</b>\nهل ترغب في تأكيد التسجيل؟", reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text in ["📥 CCP", "💳 USDT (Binance)"])
def handle_payment_method_choice(message):
    user_id = message.from_user.id
    method = message.text

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET payment_method = ?, payment_pending = 1 WHERE user_id = ?", (method, user_id))
    conn.commit()
    conn.close()

    if method == "📥 CCP":
        instruction = (
            "💸 <b>معلومات الدفع CCP:</b>\n"
            "📬 رقم CCP: <code>65 0043871362</code>\n"
            "👤 الاسم: <b>KASMI AIMEN</b>\n\n"
            "✅ بعد إتمام الدفع، أرسل <b>صورة إثبات التحويل</b> هنا."
        )
    else:
        instruction = (
            "💸 <b>معلومات الدفع USDT (TRC20):</b>\n"
            "🔗 المحفظة: <code>TXmcq5a9rDbQUwK1kL9NYVuGvL6HGnhYXB</code>\n"
            "🌐 الشبكة: TRC20\n\n"
            "✅ بعد الدفع، أرسل <b>لقطة شاشة (screenshot)</b> من عملية التحويل هنا."
        )

    bot.send_message(user_id, instruction, parse_mode="HTML")
    time.sleep(0.5)
    bot.send_message(user_id, "📸 الآن أرسل صورة إثبات الدفع:", parse_mode="HTML")
    user_states[user_id] = "awaiting_payment_proof"
@bot.message_handler(func=lambda m: m.text == "❌ إلغاء")
def cancel_selection(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET pending_vip_level = NULL, payment_method = NULL, payment_pending = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    bot.send_message(user_id, "❌ تم إلغاء اختيار العرض. يمكنك البدء من جديد.")

@bot.message_handler(func=lambda m: m.text == "✅ تأكيد التسجيل")
def confirm_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💳 الدفع عبر CCP", "🪙 الدفع عبر USDT")
    markup.row("🔙 رجوع")
    bot.send_message(message.chat.id, "💰 اختر وسيلة الدفع المناسبة لك:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["💳 الدفع عبر CCP", "🪙 الدفع عبر USDT"])
def choose_payment_method(message):
    user_id = message.from_user.id
    method = "CCP" if "CCP" in message.text else "USDT"
    
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET payment_method = ?, payment_pending = 1 WHERE user_id = ?", (method, user_id))
    conn.commit()
    conn.close()

    if method == "CCP":
        instruction = (
            "📬 <b>تفاصيل الدفع عبر CCP:</b>\n"
            "رقم الحساب: <code>65 0043871362</code>\n"
            "الاسم: <b>KASMI AIMEN</b>\n\n"
            "📸 بعد إرسال المبلغ، التقط صورة لوصل الدفع أو الشاشة وأرسلها هنا."
        )
    else:
        instruction = (
            "📬 <b>تفاصيل الدفع عبر USDT:</b>\n"
            "💼 الشبكة: <b>TRC20</b>\n"
            "🏦 عنوان المحفظة:\n<code>TYsVZ3XkJkqqt2vxuP1gZHEdZ9xGB4P4DJ</code>\n\n"
            "📸 بعد الدفع، أرسل لقطة شاشة من Binance أو صورة واضحة فيها تفاصيل التحويل."
        )

    bot.send_message(user_id, instruction, parse_mode="HTML")

@bot.message_handler(content_types=['photo'])
def receive_payment_proof(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT pending_vip_level, payment_method FROM users WHERE user_id = ? AND payment_pending = 1", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        vip, method = row
        caption = f"""🧾 طلب جديد لتأكيد الاشتراك
👤 المستخدم: @{message.from_user.username} ({user_id})
🎯 العرض: {vip}
💳 الدفع عبر: {method}
📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_{user_id}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user_id}")
        )
        bot.send_photo(ADMIN_ID, file_id, caption=caption, reply_markup=markup)
        bot.send_message(user_id, "⏳ تم إرسال إثبات الدفع. الرجاء انتظار مراجعة الإدارة.")
    else:
        bot.send_message(user_id, "⚠️ لا يوجد طلب دفع نشط أو تم بالفعل.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_") or call.data.startswith("reject_"))
def handle_admin_response(call):
    user_id = int(call.data.split("_")[1])
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    if call.data.startswith("confirm"):
        now = datetime.now().strftime('%Y-%m-%d')
        cur.execute("UPDATE users SET vip_level = pending_vip_level, pending_vip_level = NULL, subscribed = 1, payment_pending = 0, vip_start_date = ?, last_payout = ? WHERE user_id = ?",
                    (now, now, user_id))
        conn.commit()
        bot.send_message(user_id, "✅ تم تأكيد اشتراكك بنجاح! مبروك 🎉")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="✅ تم تأكيد هذا الاشتراك من طرف الإدارة.")
    else:
        cur.execute("UPDATE users SET pending_vip_level = NULL, payment_method = NULL, payment_pending = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        bot.send_message(user_id, "❌ تم رفض عملية الاشتراك. يرجى المحاولة من جديد.")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="❌ تم رفض هذا الطلب من طرف الإدارة.")
    conn.close()
@bot.message_handler(func=lambda m: m.text == "📨 رابط الإحالة")
def send_referral_link(message):
    link = f"https://t.me/irbahdzbot?start={message.from_user.id}"
    bot.send_message(message.chat.id, f"🔗 رابط الإحالة الخاص بك:\n<code>{link}</code>", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🧮 نقاطي")
def show_points(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT referral_points, referral_bonus_count FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        points, bonuses = row
        next_bonus = 20 - (points % 20)
        bot.send_message(user_id, f"🔢 نقاطك الحالية: {points}\n🎁 مكافآت تم الحصول عليها: {bonuses} (كل 20 نقطة = 1.5 USDT)\n➕ تحتاج {next_bonus} نقطة للحصول على المكافأة التالية.")
    else:
        bot.send_message(user_id, "❌ لم يتم العثور على حسابك.")

@bot.message_handler(func=lambda m: m.text == "📊 أرباحي")
def show_profits(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT vip_level, balance FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    if user and user[0]:
        vip = user[0]
        balance = user[1]
        bot.send_message(user_id, f"📈 <b>عرضك الحالي:</b> <b>{vip}</b>\n💰 <b>رصيدك:</b> <b>{balance} دج</b>", parse_mode="HTML")
    else:
        bot.send_message(user_id, "❌ لم تشترك بعد. اضغط على \"💼 التسجيل\" لاختيار عرض")

@bot.message_handler(func=lambda m: m.text == "🔙 رجوع")
def go_back_to_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💼 التسجيل", "💸 دفع الاشتراك")
    markup.row("📊 أرباحي", "🧮 نقاطي")
    markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
    bot.send_message(message.chat.id, "⬅️ تم الرجوع إلى القائمة الرئيسية.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "ℹ️ معلومات")
def show_info(message):
    text = """
📘 <b>معلومات حول بوت Irbah Cash DZ 💰🇩🇿</b>

🚀 <b>كيف يعمل البوت؟</b>
- تسجّل في أحد العروض.
- تربح نسبة شهرية ثابتة مدى الحياة (حسب العرض).
- لا تحتاج لإحالات للحصول على أرباح شهرية.

🎯 <b>نظام الإحالات:</b>
- كل شخص تسجّل برابطك = تربح <b>3 نقاط</b>
- كل 20 نقطة = <b>1.5 USDT</b> يتم إضافتها لرصيدك تلقائياً!

📦 <b>العروض المتوفرة:</b>
🔸 <b>اشتراك أول:</b> 7500 DZD → ربح 70% لمدة 3 أشهر فقط.
🔸 <b>VIP1:</b> 14,000 DZD → ربح 30% شهريًا مدى الحياة.
🔸 <b>VIP2:</b> 26,000 DZD → ربح 30% شهريًا مدى الحياة.
🔸 <b>VIP3:</b> 50,000 DZD → ربح 42% شهريًا (السحب يبدأ من الشهر 2).
🔸 <b>VIP4:</b> 110,000 DZD → ربح 43% شهريًا + 8 USDT هدية (السحب يبدأ من الشهر 2).

💬 للمزيد من التفاصيل أو الاستفسار، اتصل بنا عبر البوت.
    """
    bot.send_message(message.chat.id, text, parse_mode="HTML")
@bot.message_handler(func=lambda m: m.text == "🪙 سحب العمولة")
def request_withdraw_start(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance, subscribed FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row or row[1] != 1:
        bot.send_message(user_id, "❌ يجب أن تكون مشتركًا لتطلب السحب.")
        return

    balance = row[0]
    if balance < 1500:
        bot.send_message(user_id, "⚠️ الحد الأدنى للسحب هو 1500 دج.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📤 سحب عبر CCP", "📤 سحب عبر USDT")
    markup.row("🔙 رجوع")
    bot.send_message(user_id, f"💰 رصيدك الحالي: {balance} دج\nاختر وسيلة السحب:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["📤 سحب عبر CCP", "📤 سحب عبر USDT"])
def request_withdraw_confirm(message):
    user_id = message.from_user.id
    method = "CCP" if "CCP" in message.text else "USDT"

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cur.fetchone()[0]
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("✅ تأكيد السحب", "❌ إلغاء")
    markup.row("🔙 رجوع")
    bot.send_message(user_id, f"❗️ سيتم طلب سحب {balance} دج عبر {method}.\nهل تؤكد العملية؟", reply_markup=markup)

    # نخزن مؤقتًا طريقة السحب
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET payment_method = ? WHERE user_id = ?", (method, user_id))
    conn.commit()
    conn.close()

@bot.message_handler(func=lambda m: m.text == "✅ تأكيد السحب")
def finalize_withdrawal(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance, payment_method FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        bot.send_message(user_id, "❌ لا يمكن إتمام العملية.")
        return

    amount, method = row
    if amount < 1500:
        bot.send_message(user_id, "⚠️ الحد الأدنى للسحب هو 1500 دج.")
        return

    # تنبيه للأدمن
    caption = f"""
📤 <b>طلب سحب جديد</b>
👤 المستخدم: @{message.from_user.username} ({user_id})
💰 المبلغ: {amount} DZD
📎 الوسيلة: {method}
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ تأكيد", callback_data=f"wd_confirm_{user_id}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"wd_reject_{user_id}")
    )
    bot.send_message(ADMIN_ID, caption, parse_mode="HTML", reply_markup=markup)

    bot.send_message(user_id, "✅ تم إرسال طلبك إلى الإدارة، الرجاء الانتظار للموافقة.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("wd_confirm_") or call.data.startswith("wd_reject_"))
def handle_withdraw_admin(call):
    user_id = int(call.data.split("_")[2])
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    if "confirm" in call.data:
        cur.execute("UPDATE users SET balance = 0, last_withdraw_date = ? WHERE user_id = ?", (datetime.now().strftime('%Y-%m-%d'), user_id))
        conn.commit()
        bot.send_message(user_id, "✅ تم تحويل الأرباح. شكراً لاستخدامك Irbah Cash DZ!")
        bot.edit_message_text("✅ تم تأكيد السحب وإرسال الأرباح.", call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(user_id, "❌ تم رفض طلب السحب.")
        bot.edit_message_text("❌ تم رفض هذا الطلب من طرف الإدارة.", call.message.chat.id, call.message.message_id)
    conn.close()

@bot.message_handler(func=lambda m: m.text == "❌ إلغاء")
def cancel_action(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET pending_vip_level = NULL, payment_method = NULL, payment_pending = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    if state == "registering":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("اشتراك أول", "VIP1", "VIP2")
        markup.row("VIP3", "VIP4")
        markup.row("🔙 رجوع")
        bot.send_message(user_id, "❌ تم إلغاء التسجيل. يمكنك اختيار عرض آخر:", reply_markup=markup)

    elif state == "withdrawing":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("📤 سحب عبر CCP", "📤 سحب عبر USDT")
        markup.row("🔙 رجوع")
        bot.send_message(user_id, "❌ تم إلغاء السحب. يمكنك اختيار طريقة أخرى:", reply_markup=markup)

    else:
        # يرجع للقائمة الرئيسية
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("💼 التسجيل", "💸 دفع الاشتراك")
        markup.row("📊 أرباحي", "🧮 نقاطي")
        markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
        markup.row("ℹ️ معلومات")
        bot.send_message(user_id, "❌ تم إلغاء العملية.", reply_markup=markup)

    # نحذف السياق
    if user_id in user_states:
        del user_states[user_id]

def update_monthly_profit(user_id):
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    cur.execute("SELECT vip_level, vip_start_date, last_payout, balance FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return

    vip, vip_start_date, last_payout, balance = row

    if not vip:
        conn.close()
        return


    now = datetime.now()
    today = now.date()
    vip_date = datetime.strptime(vip_start_date, "%Y-%m-%d").date()
    last_payout_date = datetime.strptime(last_payout, "%Y-%m-%d").date() if last_payout else None

    # مايحسبش أرباح مرتين في نفس الشهر
    if last_payout_date and last_payout_date.month == today.month and last_payout_date.year == today.year:
        conn.close()
        return

    # الربح حسب VIP
    vip_percents = {
        "VIP1": 0.30,
        "VIP2": 0.30,
        "VIP3": 0.42 if (today - vip_date).days >= 30 else 0,
        "VIP4": 0.43 if (today - vip_date).days >= 30 else 0,
    }

    vip_amounts = {
        "VIP1": 14000,
        "VIP2": 26000,
        "VIP3": 50000,
        "VIP4": 110000,
    }

    if vip in vip_percents:
        percent = vip_percents[vip]
        amount = vip_amounts[vip]
        profit = int(amount * percent)

        if profit > 0:
            new_balance = balance + profit
            cur.execute("UPDATE users SET balance = ?, last_payout = ? WHERE user_id = ?", (new_balance, today.strftime("%Y-%m-%d"), user_id))
            conn.commit()

    conn.close()

# 🧠 تأكد أنك عرّفت هذا فوق
user_states = {}
ADMIN_ID = 6643841792  # ← غيره إذا حبيت

# 📥 استقبال صورة إثبات الدفع من المستخدم
@bot.message_handler(content_types=['photo'])
def handle_payment_proof(message):
    user_id = message.from_user.id
    if user_states.get(user_id) != "awaiting_payment_proof":
        return

    caption = f"📥 إثبات دفع جديد من المستخدم:\n👤 ID: {user_id}"
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_{user_id}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user_id}")
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, reply_markup=markup)

    bot.send_message(user_id, "📤 تم إرسال إثبات الدفع بنجاح.\n⏳ يرجى الانتظار حتى تتم مراجعته من طرف الإدارة.")
    user_states[user_id] = "waiting_admin_review"

# ✅ معالجة رد فعل الأدمن (تأكيد / رفض)
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_") or call.data.startswith("reject_"))
def handle_admin_action(call):
    action, user_id = call.data.split("_")
    user_id = int(user_id)

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    if action == "confirm":
        cur.execute("SELECT pending_vip_level FROM users WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if result and result[0]:
            vip = result[0]
            today = datetime.now().strftime("%Y-%m-%d")
            cur.execute("""
                UPDATE users SET 
                    vip_level = ?, 
                    subscribed = 1, 
                    vip_start_date = ?, 
                    last_payout = ?, 
                    payment_pending = 0
                WHERE user_id = ?
            """, (vip, today, today, user_id))
            bot.send_message(user_id, f"✅ تم تفعيل اشتراكك بنجاح في العرض: {vip}.\n🎉 مبروك! الآن ستبدأ في تلقي أرباحك كل شهر.")
        else:
            bot.send_message(user_id, "⚠️ تعذر تحديد العرض. يرجى المحاولة من جديد.")
    else:
        # في حالة الرفض يرجع يختار من جديد
        cur.execute("UPDATE users SET pending_vip_level = NULL, payment_pending = 0 WHERE user_id = ?", (user_id,))
        bot.send_message(user_id, "❌ تم رفض إثبات الدفع.\n🔁 يمكنك الآن اختيار عرض آخر أو إعادة المحاولة.")

    conn.commit()
    conn.close()

    # إزالة الأزرار من رسالة الأدمن
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda msg: msg.text == "💸 دفع الاشتراك")
def payment_method(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💳 CCP", callback_data="pay_ccp"),
        types.InlineKeyboardButton("💰 USDT (TRC20)", callback_data="pay_usdt")
    )
    bot.send_message(message.chat.id, "🔻 اختر وسيلة الدفع:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def send_payment_instructions(call):
    user_id = call.from_user.id
    method = call.data.split("_")[1]

    if method == "ccp":
        instruction = (
            "✅ <b>الدفع عبر CCP:</b>\n"
            "🔸 رقم الحساب: <code>65 0043871362</code>\n"
            "🔸 الاسم: <b>KASMI AIMEN</b>\n\n"
            "📸 بعد إتمام الدفع، أرسل لنا <b>صورة إيصال التحويل</b>.\n"
        )
    elif method == "usdt":
        instruction = (
            "✅ <b>الدفع عبر USDT - شبكة TRC20:</b>\n"
            "🔸 العنوان: <code>TXN2cVasZsmr7KeULj38aFQupGbAoMyGmW</code>\n"
            "📌 تأكد أن التحويل يتم عبر <b>TRC20</b>\n\n"
            "📸 بعد إتمام الدفع، أرسل لنا <b>لقطة شاشة (screenshot)</b> فيها تفاصيل التحويل."
        )

    bot.send_message(user_id, instruction, parse_mode="HTML")
    time.sleep(1)
    bot.send_message(user_id, "📥 أرسل الآن صورة إثبات الدفع للمتابعة.")
    user_states[user_id] = "awaiting_proof"

@bot.message_handler(func=lambda msg: msg.text == "🔙 إلغاء")
def cancel_selection(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT subscribed, payment_pending FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()

    if result:
        subscribed, payment_pending = result
        if subscribed:
            bot.send_message(user_id, "✅ أنت مشترك حالياً. لا يمكن الإلغاء بعد تفعيل الاشتراك.")
        elif payment_pending:
            bot.send_message(user_id, "⚠️ لا يمكنك الإلغاء حالياً، لقد قمت باختيار عرض وتنتظر مراجعة إثبات الدفع.")
        else:
            # يرجع للقائمة السابقة ويصفر العرض
            conn = sqlite3.connect("irbah.db")
            cur = conn.cursor()
            cur.execute("UPDATE users SET pending_vip_level = NULL WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()

            bot.send_message(user_id, "✅ تم إلغاء العرض بنجاح. يمكنك اختيار عرض جديد.")
            show_offers(message)  # يعيد عرض أزرار العروض
    else:
        bot.send_message(user_id, "❌ لم يتم العثور على حسابك.")
@bot.message_handler(content_types=['photo'])
def handle_proof_image(message):
    user_id = message.from_user.id

    if user_states.get(user_id) == "awaiting_proof":
        file_id = message.photo[-1].file_id
        caption = f"📥 إثبات الدفع من:\n👤 <b>{message.from_user.first_name}</b>\n"
        caption += f"🔗 @{message.from_user.username or 'بدون'}\n🆔 <code>{user_id}</code>\n\n"
        caption += "💡 راجع الإثبات واضغط على أحد الزرين:"

        # أزرار التأكيد والرفض
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_{user_id}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user_id}")
        )

        # إرسال الصورة للأدمن
        bot.send_photo(chat_id=6643841792, photo=file_id, caption=caption, reply_markup=markup, parse_mode="HTML")
        bot.send_message(user_id, "📤 تم إرسال الإثبات بنجاح، سيتم مراجعته من طرف الإدارة.")
        user_states[user_id] = "pending_review"

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_") or call.data.startswith("reject_"))
def process_admin_decision(call):
    action, user_id = call.data.split("_")
    user_id = int(user_id)

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    if action == "confirm":
        # استرجاع العرض المختار
        cur.execute("SELECT pending_vip_level FROM users WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if result and result[0]:
            vip_level = result[0]
            start_date = datetime.now().strftime("%Y-%m-%d")
            cur.execute("""
                UPDATE users SET vip_level = ?, vip_start_date = ?, subscribed = 1, pending_vip_level = NULL
                WHERE user_id = ?
            """, (vip_level, start_date, user_id))
            bot.send_message(user_id, f"✅ تم تفعيل اشتراكك في عرض <b>{vip_level}</b>. مبروك 🎉", parse_mode="HTML")
            bot.send_message(call.message.chat.id, "✅ تم تأكيد الاشتراك بنجاح.")
        else:
            bot.send_message(call.message.chat.id, "⚠️ لا يوجد عرض معلق لهذا المستخدم.")

    elif action == "reject":
        cur.execute("""
            UPDATE users SET pending_vip_level = NULL, payment_pending = 0
            WHERE user_id = ?
        """, (user_id,))
        bot.send_message(user_id, "❌ تم رفض إثبات الدفع. يرجى إعادة المحاولة أو التواصل مع الإدارة.")
        bot.send_message(call.message.chat.id, "❌ تم رفض الاشتراك.")

    conn.commit()
    conn.close()

@bot.message_handler(func=lambda m: m.text == "ℹ️ معلومات")
def info_handler(message):
    text = """
📘 <b>معلومات حول بوت Irbah Cash DZ 💰🇩🇿</b>

🚀 <b>كيف يخدم البوت؟</b>
- تسجّل في عرض من العروض المتاحة.
- تبعث إثبات الدفع للإدارة.
- يتم تفعيل اشتراكك وتبدأ تربح شهرياً نسبة من المبلغ لي دفعتو.

🎯 <b>نظام الإحالات:</b>
- كل شخص تسجلو عبر رابط الإحالة تاعك = 3 نقاط.
- عند وصولك لـ 20 نقطة تربح 1.5 USDT.
- كل ما تزيد 20 نقطة تربح 1.5 USDT أخرى تلقائياً 💸.

💼 <b>العروض المتاحة:</b>

1️⃣ <b>الاشتراك العادي</b> - 7500 دج
🔹 تربح 70% شهرياً لمدة 3 أشهر فقط.

2️⃣ <b>VIP1</b> - 14000 دج
🔹 تربح 30% شهرياً مدى الحياة.

3️⃣ <b>VIP2</b> - 26000 دج
🔹 تربح 30% شهرياً مدى الحياة.

4️⃣ <b>VIP3</b> - 50000 دج
🔹 تربح 42% شهرياً مدى الحياة.
⚠️ لا يمكنك السحب في الشهر الأول.

5️⃣ <b>VIP4</b> - 110000 دج
🔹 تربح 43% شهرياً مدى الحياة.
⚠️ لا يمكنك السحب في الشهر الأول.
🎁 <b>علاوة: 8 USDT مباشرة بعد التفعيل</b>

📩 لمزيد من المعلومات أو الاستفسارات، راسل الإدارة عبر البوت.

💡 نصيحة: كل ما تنشر رابط الإحالة تاعك أكثر، كل ما تربح أكثر.
    """
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🪙 سحب العمولة")
def request_withdraw_method(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT vip_level, balance, last_withdraw_date, vip_start_date FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()

    if not user or not user[0]:
        bot.send_message(user_id, "❌ لم تشترك بعد. لا يمكنك سحب العمولة.")
        return

    vip_level, balance, last_withdraw, vip_start = user

    if balance < 1:
        bot.send_message(user_id, "⚠️ رصيدك غير كافٍ للسحب.")
        return

    now = datetime.now()
    start_date = datetime.strptime(vip_start, "%Y-%m-%d")

    # منع السحب في الشهر الأول لعروض VIP3 و VIP4
    if vip_level in ["VIP3", "VIP4"]:
        diff = (now - start_date).days
        if diff < 30:
            bot.send_message(user_id, f"⏳ لا يمكنك السحب في الشهر الأول من عرض {vip_level}.")
            return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💳 السحب عبر CCP", "💰 السحب عبر USDT")
    markup.row("🔙 إلغاء")
    bot.send_message(user_id, "📤 اختر وسيلة السحب:", reply_markup=markup)
    user_states[user_id] = "awaiting_withdraw_method"

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "awaiting_withdraw_method")
def handle_withdraw_method(message):
    user_id = message.from_user.id
    method = message.text.strip()

    if method == "🔙 إلغاء":
        user_states.pop(user_id, None)
        bot.send_message(user_id, "✅ تم إلغاء العملية.")
        return

    if method not in ["💳 السحب عبر CCP", "💰 السحب عبر USDT"]:
        bot.send_message(user_id, "❌ اختيار غير صالح. يرجى المحاولة من جديد.")
        return

    user_states[user_id] = "awaiting_account_info"
    temp_data[user_id] = method

    prompt = "📮 أرسل رقم CCP الخاص بك (مثال: 1234567890)" if method == "💳 السحب عبر CCP" else "📮 أرسل عنوان محفظتك USDT (شبكة TRC20)"
    bot.send_message(user_id, prompt)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "awaiting_account_info")
def confirm_withdrawal_request(message):
    user_id = message.from_user.id
    info = message.text.strip()
    method = temp_data.get(user_id, "غير معروف")

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance, username FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()

    balance = user[0]
    username = user[1] or "بدون"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # تنبيه الأدمن
    admin_msg = f"""
📥 <b>طلب سحب جديد</b>
👤 المستخدم: @{username}
🆔 ID: <code>{user_id}</code>
💸 الرصيد: {balance} دج
💳 الوسيلة: {method}
📍 البيانات: <code>{info}</code>
🕒 الوقت: {date_str}
    """
    bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML")

    bot.send_message(user_id, "✅ تم إرسال طلبك إلى الإدارة.\nسيتم مراجعته في أقرب وقت.", reply_markup=main_menu())

    # إعادة ضبط الحالة
    user_states.pop(user_id, None)
    temp_data.pop(user_id, None)

    # هنا يمكنك لاحقًا خصم الرصيد أو حفظ سجل في جدول جديد `withdraw_requests`

@bot.message_handler(func=lambda m: m.text == "⚙️ لوحة التحكم" and m.from_user.id == ADMIN_ID)
def show_admin_panel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 قائمة المشتركين", "📋 طلبات السحب")
    markup.row("📈 إحصائيات", "🔙 رجوع")
    bot.send_message(message.chat.id, "📍 لوحة تحكم الأدمن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "⚙️ لوحة التحكم")
def show_admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return  # تجاهل إذا ماشي أدمن

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 قائمة المشتركين", "📋 طلبات السحب")
    markup.row("📈 إحصائيات", "🔙 رجوع")
    markup.row("📊 إحصائيات عامة")
    bot.send_message(message.chat.id, "📍 لوحة تحكم الأدمن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔙 رجوع")
def back_to_admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        show_admin_panel(message)
    else:
        send_welcome(message)  # يرجع للواجهة العادية للمستخدم

@bot.message_handler(func=lambda m: m.text == "📊 قائمة المشتركين")
def list_subscribers(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, vip_level, balance FROM users WHERE subscribed = 1")
    users = cur.fetchall()
    conn.close()

    if not users:
        bot.send_message(message.chat.id, "🚫 لا يوجد مشتركين حالياً.")
        return

    text = "<b>📊 قائمة المشتركين:</b>\n\n"
    for user in users:
        uid, username, vip, balance = user
        username = f"@{username}" if username != "بدون" else "بدون معرف"
        text += f"🧑‍💼 <b>{username}</b>\n🆔 ID: <code>{uid}</code>\n🏷️ VIP: {vip}\n💰 الرصيد: {balance} دج\n\n"

    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📋 طلبات السحب")
def list_withdraw_requests(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, method, info, amount, status FROM withdraw_requests WHERE status = 'قيد الانتظار'")
    requests = cur.fetchall()
    conn.close()

    if not requests:
        bot.send_message(message.chat.id, "📭 لا توجد طلبات سحب حالياً.")
        return

    for req in requests:
        req_id, uid, method, info, amount, status = req
        text = f"""
📋 <b>طلب سحب رقم {req_id}</b>

👤 ID المستخدم: <code>{uid}</code>
💳 الطريقة: {method}
📬 المعلومات: {info}
💰 المبلغ: {amount} دج
📌 الحالة: {status}
        """
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"accept_{req_id}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{req_id}")
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_") or call.data.startswith("reject_"))
def handle_withdraw_decision(call):
    req_id = int(call.data.split("_")[1])
    new_status = "تم الدفع" if call.data.startswith("accept_") else "مرفوض"

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE withdraw_requests SET status = ? WHERE id = ?", (new_status, req_id))
    conn.commit()
    conn.close()

    bot.answer_callback_query(call.id, f"✅ تم تحديث الحالة إلى: {new_status}")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda m: m.text == "📈 إحصائيات")
def show_statistics(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    # عدد المشتركين
    cur.execute("SELECT COUNT(*) FROM users WHERE subscribed = 1")
    total_subscribers = cur.fetchone()[0]

    # عدد المستخدمين المسجلين
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # عدد النقاط الموزعة
    cur.execute("SELECT SUM(referral_points) FROM users")
    total_points = cur.fetchone()[0] or 0

    # مجموع الأرباح المتراكمة
    cur.execute("SELECT SUM(balance) FROM users")
    total_balance = cur.fetchone()[0] or 0

    # عدد مرات علاوة الإحالة
    cur.execute("SELECT SUM(referral_bonus_count) FROM users")
    total_bonus = cur.fetchone()[0] or 0

    conn.close()

    text = f"""
📊 <b>إحصائيات البوت:</b>

👥 <b>عدد المستخدمين:</b> {total_users}
💼 <b>عدد المشتركين:</b> {total_subscribers}
🧮 <b>عدد النقاط:</b> {total_points}
🎁 <b>علاوات الإحالة:</b> {total_bonus} مرة
💰 <b>إجمالي الأرباح:</b> {total_balance:.2f} دج
    """

    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📋 طلبات السحب")
def show_withdraw_requests(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM withdraw_requests WHERE status = 'قيد الانتظار'")
    requests = cur.fetchall()
    conn.close()

    if not requests:
        bot.send_message(message.chat.id, "✅ لا توجد طلبات سحب حالياً.")
        return

    for req in requests:
        req_id, user_id, method, info, amount, status, date = req
        text = f"""
📥 <b>طلب سحب جديد</b>
🆔 <b>العضو:</b> <code>{user_id}</code>
💵 <b>المبلغ:</b> {amount} DZD
💳 <b>الطريقة:</b> {method}
🗓 <b>تاريخ الطلب:</b> {date}
📨 <b>معلومات الدفع:</b> {info}
        """

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"accept_{req_id}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{req_id}")
        )

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_") or call.data.startswith("reject_"))
def handle_withdraw_decision(call):
    req_id = int(call.data.split("_")[1])
    decision = "تم الدفع ✅" if call.data.startswith("accept_") else "❌ مرفوض"

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    # جلب معلومات الطلب
    cur.execute("SELECT user_id FROM withdraw_requests WHERE id = ?", (req_id,))
    row = cur.fetchone()
    if not row:
        bot.answer_callback_query(call.id, "❌ الطلب غير موجود.")
        conn.close()
        return

    user_id = row[0]

    # تحديث الحالة
    cur.execute("UPDATE withdraw_requests SET status = ? WHERE id = ?", (decision, req_id))
    conn.commit()
    conn.close()

    bot.answer_callback_query(call.id, "تم تحديث حالة الطلب.")
    bot.send_message(call.message.chat.id, "✅ تم تنفيذ الإجراء.")
    bot.send_message(user_id, f"📢 حالة طلب السحب: <b>{decision}</b>", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🪙 سحب العمولة")
def ask_withdraw_method(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row or row[0] < 1000:
        bot.send_message(user_id, "❌ لا يمكن سحب الأرباح حالياً. الحد الأدنى للسحب هو 1000 دج.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("📥 CCP", "💰 USDT (Binance)")
    markup.row("❌ إلغاء")
    bot.send_message(user_id, "💳 اختر طريقة السحب:", reply_markup=markup)
    user_states[user_id] = "awaiting_withdraw_method"

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "awaiting_withdraw_info")
def get_withdraw_info(message):
    user_id = message.from_user.id
    info = message.text.strip()
    withdraw_data[user_id]["info"] = info

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cur.fetchone()[0]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO withdraw_requests (user_id, method, info, amount, request_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, withdraw_data[user_id]["method"], info, balance, now))

    # تحديث الرصيد إلى 0
    cur.execute("UPDATE users SET balance = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    user_states.pop(user_id)
    withdraw_data.pop(user_id)

    bot.send_message(user_id, "✅ تم إرسال طلب السحب إلى الإدارة. سيتم مراجعته قريباً.")

    # إعلام الأدمن
    bot.send_message(ADMIN_ID, f"📬 طلب سحب جديد من المستخدم: {user_id}")

@bot.message_handler(func=lambda m: m.text == "❌ إلغاء")
def cancel_action(message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    withdraw_data.pop(user_id, None)
    bot.send_message(user_id, "❌ تم إلغاء العملية. ⬅️ الرجوع إلى القائمة الرئيسية.", reply_markup=main_menu())

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💼 التسجيل", "💸 دفع الاشتراك")
    markup.row("📊 أرباحي", "🧮 نقاطي")
    markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
    markup.row("ℹ️ معلومات")
    return markup

@bot.message_handler(func=lambda m: m.text == "📋 طلبات السحب")
def view_withdraw_requests(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM withdraw_requests WHERE status = 'قيد الانتظار' ORDER BY request_date DESC LIMIT 5")
    requests = cur.fetchall()
    conn.close()

    if not requests:
        bot.send_message(message.chat.id, "✅ لا توجد طلبات سحب حالياً.")
        return

    for req in requests:
        req_id, user_id, method, info, amount, status, date = req
        text = (
            f"📤 <b>طلب سحب</b>\n"
            f"👤 ID المستخدم: <code>{user_id}</code>\n"
            f"💰 المبلغ: <b>{amount} دج</b>\n"
            f"💳 الطريقة: <b>{method}</b>\n"
            f"ℹ️ المعلومات: <code>{info}</code>\n"
            f"📅 التاريخ: {date}"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"approve_{req_id}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{req_id}")
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_"))
def handle_withdraw_action(call):
    action, req_id = call.data.split("_")
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    cur.execute("SELECT user_id, amount FROM withdraw_requests WHERE id = ?", (req_id,))
    data = cur.fetchone()

    if data:
        user_id, amount = data

        if action == "approve":
            cur.execute("UPDATE withdraw_requests SET status = 'تم التحويل' WHERE id = ?", (req_id,))
            conn.commit()
            bot.send_message(user_id, f"✅ تم تحويل أرباحك بنجاح: {amount} دج 🎉")
            bot.answer_callback_query(call.id, "تم تأكيد السحب.")
        elif action == "reject":
            cur.execute("UPDATE withdraw_requests SET status = 'مرفوض' WHERE id = ?", (req_id,))
            conn.commit()
            bot.send_message(user_id, "❌ تم رفض طلب السحب. تأكد من المعلومات أو تواصل معنا.")
            bot.answer_callback_query(call.id, "تم رفض السحب.")
    else:
        bot.answer_callback_query(call.id, "❗ الطلب غير موجود.")
    conn.close()

@bot.message_handler(func=lambda m: m.text == "📊 قائمة المشتركين")
def list_users(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, username, first_name, vip_level, balance, referral_points, subscribed 
        FROM users 
        WHERE vip_level IS NOT NULL
        ORDER BY vip_start_date DESC
        LIMIT 10
    """)
    users = cur.fetchall()
    conn.close()

    if not users:
        bot.send_message(message.chat.id, "❌ لا يوجد مشتركين حالياً.")
        return

    text = "📋 <b>آخر المشتركين:</b>\n\n"
    for user in users:
        user_id, username, first_name, vip_level, balance, points, subscribed = user
        text += (
            f"👤 <b>{first_name}</b> | <code>{username or 'بدون'}</code>\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"🎟️ العرض: <b>{vip_level}</b>\n"
            f"💰 الرصيد: <b>{balance} دج</b>\n"
            f"🎯 النقاط: <b>{points}</b>\n"
            f"✅ مفعل: {'نعم' if subscribed else 'لا'}\n"
            f"──────────────\n"
        )

    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📋 طلبات السحب")
def show_withdraw_requests(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT id, user_id, method, info, amount, request_date
        FROM withdraw_requests
        WHERE status = 'قيد الانتظار'
        ORDER BY request_date ASC
        LIMIT 5
    """)
    requests = cur.fetchall()
    conn.close()

    if not requests:
        bot.send_message(message.chat.id, "❌ لا توجد طلبات سحب حالياً.")
        return

    for req in requests:
        req_id, user_id, method, info, amount, date = req
        text = (
            f"📤 <b>طلب سحب</b> #{req_id}\n"
            f"👤 ID: <code>{user_id}</code>\n"
            f"💳 الوسيلة: <b>{method}</b>\n"
            f"📄 التفاصيل: <code>{info}</code>\n"
            f"💰 المبلغ: <b>{amount} دج</b>\n"
            f"📅 التاريخ: {date}\n"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_withdraw:{req_id}:{user_id}:{amount}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_withdraw:{req_id}")
        )
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_withdraw"))
def confirm_withdraw(call):
    _, req_id, user_id, amount = call.data.split(":")
    req_id = int(req_id)
    user_id = int(user_id)
    amount = float(amount)

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE withdraw_requests SET status = 'تم الدفع' WHERE id = ?", (req_id,))
    cur.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

    bot.answer_callback_query(call.id, "✅ تم تأكيد السحب.")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(user_id, f"✅ تم قبول طلب سحبك بمبلغ {amount} دج.\n📤 سيتم تنفيذ الدفع قريباً.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_withdraw"))
def reject_withdraw(call):
    _, req_id = call.data.split(":")
    req_id = int(req_id)

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("UPDATE withdraw_requests SET status = 'مرفوض' WHERE id = ?", (req_id,))
    conn.commit()
    conn.close()

    bot.answer_callback_query(call.id, "❌ تم رفض الطلب.")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda m: m.text == "📊 إحصائيات عامة")
def show_stats(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()

    # عدد المستخدمين
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # عدد المشتركين حسب VIP
    vip_counts = {}
    for vip in ["اشتراك أول", "VIP1", "VIP2", "VIP3", "VIP4"]:
        cur.execute("SELECT COUNT(*) FROM users WHERE vip_level = ?", (vip,))
        vip_counts[vip] = cur.fetchone()[0]

    # عدد الطلبات حسب الحالة
    cur.execute("SELECT COUNT(*) FROM withdraw_requests WHERE status = 'تم الدفع'")
    confirmed = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM withdraw_requests WHERE status = 'مرفوض'")
    rejected = cur.fetchone()[0]

    # مجموع السحوبات المنفذة
    cur.execute("SELECT SUM(amount) FROM withdraw_requests WHERE status = 'تم الدفع'")
    total_paid = cur.fetchone()[0] or 0

    conn.close()

    text = (
        "<b>📊 إحصائيات عامة:</b>\n"
        f"👥 <b>إجمالي المستخدمين:</b> {total_users}\n\n"
        f"🏷️ <b>عدد المشتركين:</b>\n"
        f"- اشتراك أول: {vip_counts['اشتراك أول']}\n"
        f"- VIP1: {vip_counts['VIP1']}\n"
        f"- VIP2: {vip_counts['VIP2']}\n"
        f"- VIP3: {vip_counts['VIP3']}\n"
        f"- VIP4: {vip_counts['VIP4']}\n\n"
        f"💵 <b>طلبات السحب:</b>\n"
        f"✅ تم الدفع: {confirmed}\n"
        f"❌ مرفوضة: {rejected}\n"
        f"📦 المبلغ الإجمالي المدفوع: {total_paid} دج"
    )

    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🪙 سحب العمولة")
def handle_withdraw_request(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        bot.send_message(user_id, "❌ لم يتم العثور على حسابك.")
        return

    balance = row[0]
    if balance < 300:
        bot.send_message(user_id, "❌ لا يمكنك السحب الآن. الحد الأدنى هو 300 دج.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📥 عبر CCP", "💱 عبر USDT (Binance)")
    markup.row("🔙 إلغاء")
    bot.send_message(user_id, "💳 اختر وسيلة السحب:", reply_markup=markup)
    user_states[user_id] = "awaiting_withdraw_method"

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "awaiting_withdraw_method")
def process_withdraw_method(message):
    user_id = message.from_user.id
    method = message.text.strip()

    if method not in ["📥 عبر CCP", "💱 عبر USDT (Binance)"]:
        bot.send_message(user_id, "❌ اختر وسيلة صحيحة.")
        return

    withdraw_data[user_id] = {"method": method}
    user_states[user_id] = "awaiting_withdraw_info"

    label = "رقم CCP الكامل" if method == "📥 عبر CCP" else "عنوان المحفظة (TRC20)"
    bot.send_message(user_id, f"✍️ أدخل {label}:")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "awaiting_withdraw_info")
def process_withdraw_info(message):
    user_id = message.from_user.id
    withdraw_data[user_id]["info"] = message.text.strip()
    user_states[user_id] = "awaiting_withdraw_amount"
    bot.send_message(user_id, "💰 أدخل المبلغ الذي تريد سحبه بالدينار:")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "awaiting_withdraw_amount")
def process_withdraw_amount(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except:
        bot.send_message(user_id, "❌ أدخل مبلغ صحيح.")
        return

    conn = sqlite3.connect("irbah.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cur.fetchone()[0]

    if amount > balance:
        bot.send_message(user_id, "❌ المبلغ أكبر من رصيدك.")
        return

    method = withdraw_data[user_id]["method"]
    info = withdraw_data[user_id]["info"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO withdraw_requests (user_id, method, info, amount, request_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, method, info, amount, now))

    # لا ننقص الرصيد حتى يتم قبول الطلب من الأدمن
    conn.commit()
    conn.close()

    bot.send_message(user_id, "✅ تم إرسال طلبك بنجاح. سيتم مراجعته من طرف الأدمن.")

    # تنبيه الأدمن
    admin_msg = f"""
📥 <b>طلب سحب جديد</b>
👤 المستخدم: <a href="tg://user?id={user_id}">{user_id}</a>
💳 الوسيلة: {method}
📄 المعلومات: <code>{info}</code>
💰 المبلغ: {amount} دج
🕒 التاريخ: {now}
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_withdraw_{user_id}_{amount}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_withdraw_{user_id}")
    )
    bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML", reply_markup=markup)
    user_states.pop(user_id, None)
    withdraw_data.pop(user_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_withdraw_") or call.data.startswith("reject_withdraw_"))
def process_withdraw_action(call):
    data = call.data
    parts = data.split("_")
    action = parts[0]

    if action == "confirm":
        user_id = int(parts[2])
        amount = float(parts[3])

        conn = sqlite3.connect("irbah.db")
        cur = conn.cursor()

        # تحديث الطلب إلى مقبول
        cur.execute("UPDATE withdraw_requests SET status = 'مقبول' WHERE user_id = ? AND amount = ?", (user_id, amount))
        # خصم الرصيد
        cur.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))

        conn.commit()
        conn.close()

        bot.send_message(user_id, f"✅ تم قبول طلب السحب الخاص بك بمبلغ {amount} دج.")
        bot.edit_message_text("✅ تم التأكيد بنجاح.", call.message.chat.id, call.message.message_id)

    elif action == "reject":
        user_id = int(parts[2])
        conn = sqlite3.connect("irbah.db")
        cur = conn.cursor()
        cur.execute("UPDATE withdraw_requests SET status = 'مرفوض' WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        bot.send_message(user_id, "❌ تم رفض طلب السحب الخاص بك.")
        bot.edit_message_text("❌ تم الرفض.", call.message.chat.id, call.message.message_id)

# 🟢 انسخه وضعه في أي مكان وسط أو نهاية الملف مع باقي handlers
@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def handle_back(message):
    user_id = message.from_user.id
    send_main_menu(user_id)

# ✅ لوحة تحكم الأدمن
@bot.message_handler(func=lambda message: message.text == "⚙️ لوحة الأدمن" and message.from_user.id == 6643841792)
def show_admin_panel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 قائمة المشتركين", "📋 طلبات السحب")
    markup.row("🔙 رجوع")
    bot.send_message(message.chat.id, "📍 لوحة تحكم الأدمن:", reply_markup=markup)

# 🔙 زر الرجوع للقائمة الرئيسية
@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def back_to_main_menu(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💼 التسجيل", "💸 دفع الاشتراك")
    markup.row("📊 أرباحي", "🧮 نقاطي")
    markup.row("📨 رابط الإحالة", "🪙 سحب العمولة")
    markup.row("ℹ️ معلومات")

    if user_id == 6643841792:
        markup.row("⚙️ لوحة الأدمن")

    bot.send_message(user_id, "✅ تم الرجوع إلى القائمة الرئيسية.", reply_markup=markup)
# === تشغيل البوت ===
print("✅ Irbah Cash DZ Bot is running...")
bot.polling(none_stop=True)
