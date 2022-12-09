import sqlite3

def callback__(idd_):
    conn = sqlite3.connect('repo.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE order_id = '{idd_}'")
    rows = cursor.fetchall()
    print(rows[0][1])


callback__(1200)
