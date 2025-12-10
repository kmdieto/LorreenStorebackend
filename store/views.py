from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer


# ----- Web Views -----
def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


# ----- API Views -----
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductImageUploadView(generics.CreateAPIView):
    """
    Allows uploading multiple images for a single product in one request.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        images = request.FILES.getlist('images')  # multiple files key

        if not product_id or not images:
            return Response(
                {"error": "Product ID and at least one image are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_images = []
        for img in images:
            product_image = ProductImage.objects.create(product_id=product_id, image=img)
            uploaded_images.append(ProductImageSerializer(product_image).data)

        return Response(uploaded_images, status=status.HTTP_201_CREATED)
