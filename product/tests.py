from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import CategorySerializer, ProductSerializer


class CategorySerializerTest(TestCase):
    def test_retorna_campos_esperados(self):
        category = CategoryFactory()
        data = CategorySerializer(category).data
        self.assertEqual(set(data.keys()), {"title", "slug", "description", "active"})

    def test_aceita_dados_validos(self):
        serializer = CategorySerializer(data={"title": "Fantasia", "slug": "fantasia"})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()
        self.assertEqual(category.title, "Fantasia")

    def test_titulo_obrigatorio(self):
        serializer = CategorySerializer(data={"slug": "fantasia"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_rejeita_slug_repetido(self):
        CategoryFactory(slug="fantasia")
        serializer = CategorySerializer(data={"title": "Outra", "slug": "fantasia"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_retorna_campos_esperados(self):
        product = ProductFactory(category=[self.category])
        data = ProductSerializer(product).data
        self.assertEqual(
            set(data.keys()),
            {"id", "title", "description", "price", "active", "category"},
        )

    def test_categoria_aparece_dentro_do_produto(self):
        product = ProductFactory(category=[self.category])
        data = ProductSerializer(product).data
        self.assertEqual(len(data["category"]), 1)
        self.assertEqual(data["category"][0]["title"], self.category.title)

    def test_cria_produto_com_dados_validos(self):
        payload = {"title": "Duna", "price": 4990, "categories_id": [self.category.id]}
        serializer = ProductSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.title, "Duna")
        self.assertEqual(list(product.category.all()), [self.category])

    def test_titulo_obrigatorio(self):
        serializer = ProductSerializer(data={"price": 4990, "categories_id": []})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_rejeita_preco_zero(self):
        serializer = ProductSerializer(data={"title": "Duna", "price": 0, "categories_id": []})
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_rejeita_categoria_inexistente(self):
        serializer = ProductSerializer(
            data={"title": "Duna", "price": 4990, "categories_id": [999]}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("categories_id", serializer.errors)