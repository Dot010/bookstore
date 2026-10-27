import pytest

from product.factories import CategoryFactory, ProductFactory
from product.serializers import CategorySerializer, ProductSerializer


@pytest.mark.django_db
def test_category_serializer():
    category = CategoryFactory()

    data = CategorySerializer(category).data

    assert data["title"] == category.title
    assert data["slug"] == category.slug
    assert data["active"] == category.active


@pytest.mark.django_db
def test_product_serializer_com_categorias():
    fantasia = CategoryFactory()
    aventura = CategoryFactory()
    product = ProductFactory(category=[fantasia, aventura])

    data = ProductSerializer(product).data

    assert data["title"] == product.title
    assert data["price"] == product.price
    assert len(data["category"]) == 2