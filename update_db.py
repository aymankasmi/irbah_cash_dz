import sqlite3

def add_column_if_not_exists(cursor, table, column, col_type):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        print(f"✅ تم إضافة العمود: {column}")
    else:
        print(f"⚠️ العمود {column} موجود من قبل.")

conn = sqlite3.connect("irbah.db")
cur = conn.cursor()

add_column_if_not_exists(cur, "users", "pending_vip_level", "TEXT")
add_column_if_not_exists(cur, "users", "payment_method", "TEXT")
add_column_if_not_exists(cur, "users", "payment_pending", "INTEGER DEFAULT 0")

conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("irbah.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS withdraw_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    method TEXT,
    info TEXT,
    amount REAL,
    status TEXT DEFAULT 'قيد الانتظار',
    request_date TEXT
)
""")

conn.commit()
conn.close()
print("✅ تم التحقق من جدول withdraw_requests.")
