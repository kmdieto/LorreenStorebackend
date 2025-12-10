from django.urls import path
from .views import (
    ProductListCreateView,
    CategoryListCreateView,
    ProductImageUploadView,
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('upload-images/', ProductImageUploadView.as_view(), name='upload-images'),
]
