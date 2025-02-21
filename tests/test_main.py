import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Database
import sqlite3

client = TestClient(app)
db = Database()

@pytest.fixture(scope="function")
def setup_db():
    """Fixture para configurar o banco de dados temporário em memória para testes."""
    db.init_db()
    yield
    # Limpar o banco de dados após os testes
    conn = sqlite3.connect(db.db_name)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS favorites")
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()

def test_read_root(setup_db):
    """Teste para a rota raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao escambo zap!"}

def test_get_products(setup_db):
    """Teste para a rota de obter produtos."""
    response = client.get("/products/")
    assert response.status_code == 200
    json_response = response.json()
    assert "products" in json_response
    assert isinstance(json_response["products"], list)

def test_buy_product(setup_db):
    """Teste para a rota de comprar produto."""
    response = client.post("/buy/", json={"product_id": 1, "user_id": 1})
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_transactions(setup_db):
    """Teste para a rota de obter transações."""
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_login(setup_db):
    """Teste para a rota de login."""
    response = client.post("/login", json={"user_phone": "+14155552671"})
    assert response.status_code == 200
    assert "message" in response.json()

def test_process_payment(setup_db):
    """Teste para a rota de processar pagamento."""
    response = client.post("/pay", json={"user": "user1", "amount": 100.0})
    assert response.status_code == 200
    assert "message" in response.json()