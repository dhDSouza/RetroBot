import sqlite3

from datetime import datetime, timedelta


def connect_db():

    return sqlite3.connect('bot.db')


def create_tables():
    with connect_db() as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        discord_id TEXT PRIMARY KEY,
                        ra_username TEXT
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS challenges (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        console_name TEXT,
                        game_name TEXT,
                        game_id INTEGER,
                        console_image_url TEXT,
                        game_image_url TEXT,
                        start_date TEXT,
                        end_date TEXT,
                        is_open INTEGER DEFAULT 1
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    achievement_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(discord_id)
                )''')

        c.execute('''CREATE TABLE IF NOT EXISTS challenge_players (
                    user_id TEXT, 
                    challenge_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(discord_id),
                    FOREIGN KEY (challenge_id) REFERENCES challenges(id),
                    PRIMARY KEY (user_id, challenge_id)
                )''')

        conn.commit()


def register_user(discord_id, ra_username):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute("INSERT OR REPLACE INTO users (discord_id, ra_username) VALUES (?, ?)",
                  (discord_id, ra_username))
        conn.commit()


def get_ra_username(discord_id):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute(
            "SELECT ra_username FROM users WHERE discord_id = ?", (discord_id,))

        result = c.fetchone()

        return result[0] if result else None


def get_all_users():
    with connect_db() as conn:
        c = conn.cursor()

        c.execute("SELECT discord_id, ra_username FROM users")

        users = c.fetchall()

        return users


def add_challenge(console_name, game_name, game_id, console_image_url, game_image_url):
    with connect_db() as conn:
        c = conn.cursor()

        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)

        c.execute('''INSERT INTO challenges (console_name, game_name, game_id, console_image_url, game_image_url, start_date, end_date, is_open)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (console_name, game_name, game_id, console_image_url,
                   game_image_url, start_date, end_date, 1)
                  )

        conn.commit()


def get_current_challenge():
    with connect_db() as conn:
        c = conn.cursor()

        c.execute('''SELECT * FROM challenges 
                     WHERE start_date <= datetime('now') 
                     AND end_date >= datetime('now') 
                    ORDER BY id DESC LIMIT 1;''')

        result = c.fetchone()

        if result:
            return {
                "id": result[0],
                "console_name": result[1],
                "game_name": result[2],
                "game_id": result[3],
                "console_image_url": result[4],
                "game_image_url": result[5],
                "start_date": result[6],
                "end_date": result[7],
                "is_open": result[8]
            }
        else:
            return None


def check_challenge_status():
    with connect_db() as conn:
        c = conn.cursor()

        c.execute('''SELECT * FROM challenges 
                    WHERE start_date <= datetime('now') 
                    AND end_date <= datetime('now') 
                    ORDER BY id DESC LIMIT 1;''')

        result = c.fetchone()

        if result:
            return {
                "id": result[0],
                "console_name": result[1],
                "game_name": result[2],
                "game_id": result[3],
                "console_image_url": result[4],
                "game_image_url": result[5],
                "start_date": result[6],
                "end_date": result[7],
                "is_open": result[8]
            }
        else:
            return None


def finish_challenge(id):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute("UPDATE challenges SET is_open = 0 WHERE id = ?", (id,))
        conn.commit()
        rows_affected = c.rowcount

        return rows_affected > 0


def update_challenge(new_challenge):
    with connect_db() as conn:
        c = conn.cursor()

        current_challenge = get_current_challenge()

        if current_challenge:
            c.execute('''UPDATE challenges SET console_name = ?, game_name = ?, game_id = ?, console_image_url = ?, game_image_url = ?, start_date = ?, end_date = ?, is_open = ? WHERE id = ?''',
                      (new_challenge['console'], new_challenge['game'], new_challenge['game_id'], new_challenge['console_image_url'], new_challenge['game_image_url'], datetime.now(), datetime.now() + timedelta(days=7), 1, current_challenge['id']))

            conn.commit()

            if c.rowcount > 0:

                return True
            else:

                return False
        else:
            print("Não há um desafio ativo para ser atualizado.")

            return False


def save_achievement(user_id, achievement_id):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute("SELECT * FROM achievements WHERE user_id = ? AND achievement_id = ?",
                  (user_id, achievement_id))
        exists = c.fetchone()

        if exists is None:
            c.execute('INSERT INTO achievements (user_id, achievement_id) VALUES (?, ?)',
                      (user_id, achievement_id))
            conn.commit()
        else:
            print(
                f"A conquista {achievement_id} já está registrada para o usuário {user_id}.")


def get_user_achievements(user_id):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute(
            "SELECT achievement_id FROM achievements WHERE user_id = ?", (user_id,))
        rows = c.fetchall()

        return [row[0] for row in rows]


def register_participation(discord_id, challenge_id):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute(
            "INSERT INTO challenge_players (user_id, challenge_id) VALUES (?, ?)", (discord_id, challenge_id))
        conn.commit()


def get_participating_users(challenge_id):
    with connect_db() as conn:
        c = conn.cursor()

        c.execute(
            '''SELECT user_id FROM challenge_players WHERE challenge_id = ?''', (challenge_id,))

        participants = c.fetchall()

        return [row[0] for row in participants] if participants else []
