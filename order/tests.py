import pytest

from order.factories import OrderFactory
from order.serializers import OrderSerializer
from product.factories import ProductFactory


@pytest.mark.django_db
def test_order_total():
    p1 = ProductFactory(price=100)
    p2 = ProductFactory(price=200)
    order = OrderFactory(product=[p1, p2])

    data = OrderSerializer(order).data

    assert len(data["product"]) == 2
    assert data["total"] == 300


@pytest.mark.django_db
def test_order_sem_produtos():
    order = OrderFactory()

    data = OrderSerializer(order).data

    assert data["product"] == []
    assert data["total"] == 0