from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(price=100)
        self.order = OrderFactory(user=self.user, product=[self.product])

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