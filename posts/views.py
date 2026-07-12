from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrModerator

# ==========================================
# POSTS (Feed, Profilo, CRUD)
# ==========================================
class FeedView(generics.ListAPIView):
    """Gestisce la visualizzazione di tutti i post (feed generale)"""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonalFeedView(generics.ListAPIView):
    """Gestisce la visualizzazione dei post dei soli utenti che seguo (feed personale)"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        utenti_seguiti = self.request.user.following.values_list('followed', flat=True)
        return Post.objects.filter(author__in=utenti_seguiti).order_by('-created_at')

class ProfileView(generics.ListCreateAPIView):
    """Gestisce la visualizzazione dei soli post dell'utente (profilo personale) e la creazione di nuovi"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Gestisce la lettura, modifica e cancellazione di un SINGOLO post tramite ID"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModerator]

# ==========================================
# COMMENTS (Cronologia, Sezione commenti, CRUD)
# ==========================================
class CommentHistoryListView(generics.ListAPIView):
    """Gestisce la visualizzazione della cronologia dei commenti dell'utente"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by('-created_at')

class CommentSectionView(generics.ListCreateAPIView):
    """Gestisce la visualizzazione dei commenti di un post specifico (sezione commenti del post) e l'aggiunta di un nuovo commento"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id']).order_by('-created_at')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Gestisce la lettura, modifica e cancellazione di un commento specifico per un post specifico"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModerator]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

# ==========================================
# LIKES (Cronologia e Toggle)
# ==========================================
class LikeHistoryView(generics.ListAPIView):
    """Gestisce la visualizzazione della cronologia dei post a cui l'utente ha messo like"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModerator]

    def get_queryset(self):
        return Post.objects.filter(likes__user=self.request.user).order_by('-likes__created_at')

class LikeToggleView(generics.CreateAPIView):
    """Gestisce il toggle (aggiungi/rimuovi) del like ad un post specifico"""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like_esistente = Like.objects.filter(user=request.user, post=post).first()

        if like_esistente:
            like_esistente.delete()
            return Response(
                {"status": f"Like rimosso dal post {post_id}"}, 
                status=status.HTTP_200_OK
            )
        else:
            nuovo_like = Like.objects.create(user=request.user, post=post)
            serializer = self.get_serializer(nuovo_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)