import os
import sqlite3
import logging
from dotenv import load_dotenv
import subprocess

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificar se as variáveis de ambiente estão configuradas
required_env_vars = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER"]
for var in required_env_vars:
    if not os.getenv(var):
        logger.error(f"Variável de ambiente {var} não está configurada.")
        exit(1)

# Inicializar o banco de dados
db_name = 'escambozap.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Criar tabelas
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

# Popular o banco com dados fictícios
cursor.execute("INSERT INTO products (name, price, description) VALUES ('Produto 1', 10.0, 'Descrição do Produto 1')")
cursor.execute("INSERT INTO products (name, price, description) VALUES ('Produto 2', 20.0, 'Descrição do Produto 2')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'password1')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user2', 'password2')")
conn.commit()
conn.close()

# Rodar o servidor Uvicorn
subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])