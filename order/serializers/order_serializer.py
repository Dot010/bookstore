from rest_framework import serializers

from order.models.order import Order
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True, allow_empty=False
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "product", "products_id", "total"]

    def get_total(self, instance):
        return sum(product.price or 0 for product in instance.product.all())

    def create(self, validated_data):
        products = validated_data.pop("products_id")
        order = Order.objects.create(**validated_data)
        order.product.set(products)
        return order