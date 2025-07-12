import sqlite3

conn = sqlite3.connect("irbah.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(users)")
columns = cur.fetchall()
conn.close()

print("📋 أعمدة جدول users:")
for col in columns:
    print(f"- {col[1]}")
