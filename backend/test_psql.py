import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="live_ai_assistent",  # or live_ai_assistent if that's the actual name
        user="postgres",
        password="1234",
    )

    print("✅ Connected Successfully!")

    cur = conn.cursor()
    cur.execute("SELECT current_database();")
    print("Database:", cur.fetchone())

    conn.close()

except Exception as e:
    print("❌ Error:")
    print(e)