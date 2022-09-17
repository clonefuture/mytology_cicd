from rest_framework import serializers

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for pos in positions:
            addr = Stock.objects.get(address=validated_data['address'])
            stock_prod, created = StockProduct.objects.update_or_create(product=pos['product'],
                                                                        quantity=pos['quantity'],
                                                                        price=pos['price'],
                                                                        stock=addr)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for pos in positions:
            stock_prod, created = StockProduct.objects.update_or_create(product=pos['product'],
                                                                        stock=stock,
                                                                        defaults={'quantity': pos['quantity'],
                                                                                  'price': pos['price']}
                                                                        )

        return stock
