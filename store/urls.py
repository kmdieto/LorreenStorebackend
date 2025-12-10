from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Web routes for store (login, home)
    path('', include('store.urls')),

    # API routes for store endpoints
    path('api/', include('store.urls')),  # ✅ Add this line
]
