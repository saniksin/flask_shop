from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from src.apps.product.serializers import *
from src.apps.product.models import *


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retvieve']:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    

class IndexView(TemplateView):
    template_name = "index.html"