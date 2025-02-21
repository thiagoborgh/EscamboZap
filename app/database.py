import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name='escambozap.db'):
        self.db_name = db_name

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                buyer_id INTEGER NOT NULL,
                seller_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (buyer_id) REFERENCES users (id),
                FOREIGN KEY (seller_id) REFERENCES users (id)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_products_name ON products (name)
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_product_id ON transactions (product_id)
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_buyer_id ON transactions (buyer_id)
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_seller_id ON transactions (seller_id)
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites (user_id)
            ''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_favorites_product_id ON favorites (product_id)
            ''')
            conn.commit()