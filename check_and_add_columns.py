import sqlite3

# نفتح اتصال بقاعدة البيانات
conn = sqlite3.connect("irbah.db")
cur = conn.cursor()

# الأعمدة المطلوبة
required_columns = [
    "user_id", "username", "first_name", "referrer_id",
    "referral_points", "vip_level", "subscribed", "vip_start_date",
    "last_payout", "balance", "last_withdraw_date",
    "referral_bonus_count", "total_rewards"
]

# نجيب الأعمدة الموجودة
cur.execute("PRAGMA table_info(users)")
existing_columns = [col[1] for col in cur.fetchall()]

# نضيف الأعمدة الناقصة
for column in required_columns:
    if column not in existing_columns:
        # نوع البيانات حسب العمود
        if column in ["vip_level", "referral_points", "subscribed", "referral_bonus_count"]:
            column_type = "INTEGER"
        elif column in ["vip_start_date", "last_payout", "last_withdraw_date"]:
            column_type = "TEXT"
        elif column in ["balance", "total_rewards"]:
            column_type = "REAL"
        else:
            column_type = "TEXT"

        alter_query = f"ALTER TABLE users ADD COLUMN {column} {column_type}"
        cur.execute(alter_query)
        print(f"✅ تم إضافة العمود: {column}")

conn.commit()
conn.close()
print("✅ الفحص واكتمال الأعمدة تم بنجاح.")
