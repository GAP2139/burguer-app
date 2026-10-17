import os 
import sys
import pytest


sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import serialize_user

@pytest.mark.parametrize("user, esperado",     [
    (
        {
            "email": "teste@exemplo.com",
            "name": "Teste Usuário",
            "address": "123 Rua Exemplo",
            "role": "admin"
        },
        {
            "email": "teste@exemplo.com",
            "name": "Teste Usuário",
            "address": "123 Rua Exemplo",
            "role": "admin"
        }
    ),
    (
        {
            "email": "teste@exemplo.com"
        },
        {
            "email": "teste@exemplo.com",
            "name": "",
            "address": "",
            "role": "cliente"
        }
    ),
    (
        {},
        {
            "email": None,
            "name": "",
            "address": "",
            "role": "cliente"
        }
    ),
    (
        {
            "email": None,
            "name": None,
            "address": None,
            "role": None
        },
        {
            "email": None,
            "name": None,
            "address": None,
            "role": None
        }
    ),
    (
        {
            "email": 123,
            "name": ["Teste", "Usuário"],
            "address": {"street": "123 Rua Exemplo"},
            "role": True
        },
        {
            "email": 123,
            "name": ["Teste", "Usuário"],
            "address": {"street": "123 Rua Exemplo"},
            "role": True
        }
    )
])

def test_serialize_user_parametrizado(user,esperado):
    resultado = serialize_user(user)
    assert resultado == esperado

@pytest.mark.parametrize("entrada", [
    None,
    "string",
    123456,
    []
])

def test_serialize_user_parametrizado_excecao(entrada):
    with pytest.raises(AttributeError):
        serialize_user(entrada)
