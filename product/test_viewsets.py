from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Category, Product


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory(title="Fantasia")

    def test_lista_categorias(self):
        url = reverse("category-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Fantasia")

    def test_cria_categoria(self):
        url = reverse("category-list")
        data = {"title": "Terror", "slug": "terror"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.product = ProductFactory(title="Duna", price=100, category=[self.category])

    def test_lista_produtos(self):
        url = reverse("product-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Duna")

    def test_cria_produto(self):
        url = reverse("product-list")
        data = {"title": "1984", "price": 3990, "categories_id": [self.category.id]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_rejeita_preco_zero(self):
        url = reverse("product-list")
        data = {"title": "Grátis", "price": 0, "categories_id": [self.category.id]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)