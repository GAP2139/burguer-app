import pytest 
import requests
from unittest.mock import patch, Mock
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


load_dotenv()

# @pytest.fixture(scope="session")
# def mongo_client():
#     uri = os.getenv("MONGO_URI")
#     client = MongoClient(uri)
#     yield client
#     client.close()


# @pytest.fixture(scope="function")
# def test_db(mongo_client):
#     db = mongo_client["burguer_app_test"]

#     db["users"].delete_many({})
#     db["pedidos"].delete_many({})
#     yield db


@pytest.fixture
def base_urls():
    """Retorna a URL base da aplicação para testes"""
    return {
        "order": "http://localhost:5000/auth",
        "user": "http://localhost:5001/user",
        "order_url": "http://localhost:5002/order",
        "product_url": "http://localhost:5003/product",
            }


@pytest.fixture
def sample_user():
    """Retorna um usuário de exemplo para os testes"""
    return {
        "email": "cliente@teste.com",
        "password": "senha123",
        "name": "Cliente Teste",
        "address": "Rua Teste, 123",
        "role": "cliente"
    }


@pytest.fixture
def sample_items():
    return {
        "item_name": ["Hambúrguer Teste", "Refrigerante Teste"],
        "item_price": [10.0, 5.0],
        "quantity": ["2", "1"]
    }


@pytest.fixture
def mock_user_service():
    """Mock do serviço de usuário para testes"""
    with patch(requests.get) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "cliente@teste.com",
            "name": "Cliente Teste",
            "address": "Rua Teste, 123",
            "role": "cliente"
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_order_service():
    """Mock do serviço de pedidos para testes"""
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {"location": "/order/list"}
        mock_post.return_value = mock_response
        yield mock_post


def check_service_health(url):
    """Verifica a saúde do serviço"""
    try:
        response = requests.get(f"{url}/", timeout=2)
        return response.status_code in [200,302,404]
    except requests.exceptions.ConnectionError:
        return False


@pytest.fixture
def services_running(base_urls):
    """Verifica quais serviços estão rodando"""
    return {
        service: check_service_health(url)
        for service, url in base_urls.items()
    }


@pytest.fixture
def skip_if_services_down(services_running):
    """Pula testes se os serviços não estiverem rodando"""
    def _skip_if_down(*required_services):
        for service in required_services:
            if not services_running.get(f"{service}_url", False):
                pytest.skip(f"Serviço {service} não está rodando")
    return _skip_if_down