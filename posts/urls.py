from django.urls import path
from . import views

urlpatterns = [
    # --- POSTS ---
    path('posts/', views.FeedView.as_view(), name='feed'),
    path('posts/profile/', views.ProfileView.as_view(), name='profile'),
    path('posts/personal_feed/', views.PersonalFeedView.as_view(), name='personal_feed'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    # --- COMMENTS (Rotte Annidate e Cronologia) ---
    path('comments/history/', views.CommentHistoryListView.as_view(), name='comment_history'),
    path('posts/<int:post_id>/comments/', views.CommentSectionView.as_view(), name='post_comment_section'),
    path('posts/<int:post_id>/comments/<int:pk>/', views.CommentDetailView.as_view(), name='post_comment_detail'),

    # --- LIKES ---
    path('likes/', views.LikeHistoryView.as_view(), name='like_history'),
    path('posts/<int:post_id>/like/', views.LikeToggleView.as_view(), name='post_like_toggle'),
]