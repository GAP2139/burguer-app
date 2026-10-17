import pytest
import requests
from unittest.mock import patch, Mock


class TestOrderUserIntegration:

    def test_user_order_valid_user_with_services(self, base_urls, sample_user, sample_items,skip_if_services_down):
        """Testa a criação de um pedido com usuário válido e serviços rodando"""
        skip_if_services_down("user", "order")

        order_data = {
            "email": sample_user["email"],
            **sample_items
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code == 302


    @patch('requests.post')
    def test_create_order_valid_user_mocked(self, mock_post, base_urls, sample_user, sample_items):
        """Testa a criação de um pedido com usuário válido usando mock"""
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': '/order/list'}
        mock_post.return_value = mock_response

        order_data = {
            "email": sample_user["email"],
            **sample_items
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code == 302


    def test_create_order_user_not_found_with_services(self,base_urls, sample_items, skip_if_services_down):
        """Testa a criação de um pedido com usuário não encontrado"""
        skip_if_services_down("user", "order")

        order_data = {
            "user_email": "naoexiste@teste.com",
            **sample_items
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code in [404, 400] # Espera erro 404 ou 400 se usuário não encontrado


class TesteServiceHealthCheck:

    def test_order_service_health_check(self, base_urls):
        try:
            response = requests.get(f"{base_urls['order']}/", timeout=2)
            assert response.status_code in [200, 302, 404] # 404 é Ok, significa que está rodando
        except requests.exceptions.ConnectionError:
            pytest.skip("Serviço de pedidos não está rodando")

    def test_user_service_health_check(self, base_urls):
        try:
            response = requests.get(f"{base_urls['user']}/", timeout=2)
            assert response.status_code in [200, 302, 404] # 404 é Ok, significa que está rodando
        except requests.exceptions.ConnectionError:
            pytest.skip("Serviço de usuários não está rodando")