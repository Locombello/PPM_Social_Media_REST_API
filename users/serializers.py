from rest_framework import serializers
from .models import CustomUser, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'bio']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            bio=validated_data.get('bio', ''),
            role='standard'  # Ruolo standard di default
        )
        return user

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    followed = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']

    def validate(self, data):
        request_user = self.context['request'].user
        
        if request_user == data['followed']:
            raise serializers.ValidationError({"followed": "Non puoi seguire te stesso!"})
            
        return data