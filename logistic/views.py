from rest_framework.viewsets import ModelViewSet

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('title')
    serializer_class = ProductSerializer
    search_fields = ['title']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    search_fields = ['$products__title', '$products__description']
    filterset_fields = ['products']
