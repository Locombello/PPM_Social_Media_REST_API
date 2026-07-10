from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    # Autore in sola lettura in modo che l'utente non possa fingere di essere qualcun altro
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'post', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # Commenti inclusi direttamente nel dettaglio del post
    comments = CommentSerializer(many=True, read_only=True)
    # Campo calcolato per il numero di like
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'comments', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']