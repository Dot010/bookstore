from django.test import TestCase

from order.factories import OrderFactory, UserFactory
from order.serializers import OrderSerializer
from product.factories import ProductFactory


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.p1 = ProductFactory(price=100)
        self.p2 = ProductFactory(price=250)

    def test_retorna_campos_esperados(self):
        order = OrderFactory(user=self.user, product=[self.p1])
        data = OrderSerializer(order).data
        self.assertEqual(set(data.keys()), {"id", "user", "product", "total"})

    def test_total_soma_os_produtos(self):
        order = OrderFactory(user=self.user, product=[self.p1, self.p2])
        data = OrderSerializer(order).data
        self.assertEqual(data["total"], 350)

    def test_cria_pedido_com_dados_validos(self):
        payload = {"user": self.user.id, "products_id": [self.p1.id, self.p2.id]}
        serializer = OrderSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.product.count(), 2)

    def test_rejeita_pedido_sem_produtos(self):
        serializer = OrderSerializer(data={"user": self.user.id, "products_id": []})
        self.assertFalse(serializer.is_valid())
        self.assertIn("products_id", serializer.errors)

    def test_usuario_obrigatorio(self):
        serializer = OrderSerializer(data={"products_id": [self.p1.id]})
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
