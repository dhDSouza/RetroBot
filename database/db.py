import sqlite3

def connect_db():
    conn = sqlite3.connect('bot.db')
    return conn

def create_tables():
    conn = connect_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    discord_id TEXT PRIMARY KEY,
                    ra_username TEXT
                )''')

    conn.commit()
    conn.close()

def register_user(discord_id, ra_username):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (discord_id, ra_username) VALUES (?, ?)", (discord_id, ra_username))
    conn.commit()
    conn.close()

def get_ra_username(discord_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT ra_username FROM users WHERE discord_id = ?", (discord_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_all_users():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT discord_id, ra_username FROM users")
    users = c.fetchall()
    conn.close()
    return users
