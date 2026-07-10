from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    # Registrazione e Accesso
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Seguiti e Follower
    path('users/following/', views.FollowedListView.as_view(), name='following'),
    path('users/followers/', views.FollowerListView.as_view(), name='followers'),
    path('users/following/<int:user_id>/', views.FollowedDetailView.as_view(), name='followed_detail'),
    path('users/followers/<int:user_id>/', views.FollowerDetailView.as_view(), name='follower_detail'),

    # Utenti
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
]