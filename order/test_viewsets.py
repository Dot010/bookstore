from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(price=100)
        self.order = OrderFactory(user=self.user, product=[self.product])
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_lista_pedidos(self):
        url = reverse("order-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["total"], 100)

    def test_cria_pedido(self):
        url = reverse("order-list")
        data = {"user": self.user.id, "products_id": [self.product.id]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_sem_token_recebe_401(self):
        self.client.credentials()
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenAuthTest(APITestCase):
    def test_gera_token_com_usuario_e_senha(self):
        User.objects.create_user(username="ana", password="Senha-forte-123")
        response = self.client.post(
            reverse("api-token-auth"),
            {"username": "ana", "password": "Senha-forte-123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
