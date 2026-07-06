from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Includiamo le rotte della nostra API per post, commenti e follow
    path('api/', include('posts.urls')),
    
    # Endpoint per l'autenticazione JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Questo è il login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]