from fastapi import FastAPI
from dotenv import load_dotenv
import logging
import os
from app.routes import products, users, transactions, payments
from app.database import Database

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificar se as variáveis de ambiente estão carregadas corretamente
logger.info(f"TWILIO_ACCOUNT_SID: {os.getenv('TWILIO_ACCOUNT_SID')}")
logger.info(f"TWILIO_AUTH_TOKEN: {os.getenv('TWILIO_AUTH_TOKEN')}")

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])

# Inicializar o banco de dados ao iniciar a aplicação
db = Database()
db.init_db()

