from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

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


class ProductListView(ListView):
    template_name = "product_list.html"
    model = Product
    queryset = Product.objects.filter(is_active=True)
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[Any]:
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")

        if subcategory_slug:
            products = Product.objects.filter(category__slug=subcategory_slug, is_active=True)
        elif category_slug:
            products = Product.objects.filter(category__parent__slug=category_slug, is_active=True)
        else:
            products = Product.objects.filter(is_active=True)

        return products
    

    def get_context_data(self, **kwargs: Any):
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")
        text = ""
        context = super().get_context_data(**kwargs)
        if subcategory_slug:
            subcategory = Category.objects.get(slug=subcategory).select_related("parent")

            if "Мужская" in subcategory.parent.name:
                text = f"Мужские {subcategory.name}"
            elif "Женская" in subcategory.parent.name:
                text = f"Женские {subcategory.name}"
            elif "Детская" in subcategory.parent.name:
                text = f"Детские {subcategory.name}"

        elif category_slug:
            category = Category.objects.get(slug=category_slug)
            text = category.name
        
        context["category_name"] = text
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    queryset = Product.objects.filter(is_active=True)
    context_object_name = "product"