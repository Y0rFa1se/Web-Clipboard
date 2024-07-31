from flask import g
import sqlite3

class DB:
    db_path = ""

    @classmethod
    def configure(cls, SETTINGS):
        cls.db_path = SETTINGS["DB_PATH"]

        with sqlite3.connect(cls.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
CREATE TABLE IF NOT EXISTS clipboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT NOT NULL
);
""")
            conn.commit()
            cur.close()

    @staticmethod
    def get_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(DB.db_path)

        return db
    
    @staticmethod
    def get_names():
        with DB.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM clipboard")
            names = cur.fetchall()
            cur.close()

        return names
    
    @staticmethod
    def get_content_type(name, password):
        with DB.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT type FROM clipboard WHERE name = ? AND password = ?", (name, password))
            content_type = cur.fetchone()
            cur.close()

        return content_type[0]
    
    @staticmethod
    def get(name, password):
        try:
            with DB.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT content FROM clipboard WHERE name = ? AND password = ?", (name, password))
                content = cur.fetchone()
                cur.close()

            return content[0]
        
        except:
            return None
        
    @staticmethod
    def exists(name):
        with DB.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM clipboard WHERE name = ?", (name,))
            name = cur.fetchone()
            cur.close()

        return name is not None
    
    @staticmethod
    def upload(name, password, content, content_type):
        try:
            with DB.get_db() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO clipboard (name, password, content, type) VALUES (?, ?, ?, ?)",
                            (name, password, content, content_type))
                conn.commit()
                cur.close()

            return True

        except:
            return False
        
    @staticmethod
    def delete(name, password):
        try:
            with DB.get_db() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM clipboard WHERE name = ? AND password = ?", (name, password))
                conn.commit()
                cur.close()

            return True
        
        except:
            return False