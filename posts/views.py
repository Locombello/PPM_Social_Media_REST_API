from rest_framework import viewsets, permissions
from .models import Post, Comment, Follow
from .serializers import PostSerializer, CommentSerializer, FollowSerializer
from .permissions import IsAuthorOrModerator

class PostViewSet(viewsets.ModelViewSet):
    # ModelViewSet crea in automatico gli endpoint per List, Retrieve, Create, Update e Destroy 
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModerator]

    def perform_create(self, serializer):
        # Quando viene creato un nuovo post, assegniamo automaticamente l'autore all'utente che fa la richiesta
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModerator]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModerator]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)