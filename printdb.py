import sqlite3 as lite

conn = lite.connect('db.sqlite3')
cur = conn.cursor()

def get_posts():
    with conn:
        cur.execute("SELECT * FROM auth_user")
        print(cur.fetchall())

get_posts()