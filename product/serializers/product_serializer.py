from rest_framework import serializers

from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    categories_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "categories_id",
        ]

    def validate_price(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value

    def create(self, validated_data):
        categories = validated_data.pop("categories_id")
        product = Product.objects.create(**validated_data)
        product.category.set(categories)
        return product
