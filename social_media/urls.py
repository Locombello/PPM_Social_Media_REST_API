from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # endpoint dell'API per la sezione di amministrazione
    path('admin/', admin.site.urls),
    
    # endpoint dell'API per l'app posts
    path('api/', include('posts.urls')),
    # endpoint dell'API per l'app users
    path('api/', include('users.urls')),
]