from rest_framework import serializers
from .models import User, Article, Comment, FeatureFlag

class UserSerializer(serializers.ModelSerializer):
    # Explicitly specify role in serializer (can be optional on create)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='Member')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'tags', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'created_at']

class FeatureFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlag
        fields = ['id', 'name', 'is_enabled']
