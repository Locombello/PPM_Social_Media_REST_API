from rest_framework import serializers
from .models import Post, Comment, Like, Follow

class CommentSerializer(serializers.ModelSerializer):
    # Autore in sola lettura in modo che l'utente non possa fingere di essere qualcun altro
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        read_only_fields = ['post']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # Commenti inclusi direttamente nel dettaglio del post
    comments = CommentSerializer(many=True, read_only=True)
    # Campo calcolato per il numero di like
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']