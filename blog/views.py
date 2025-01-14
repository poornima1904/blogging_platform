from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Article, Comment, FeatureFlag
from .serializers import UserSerializer, ArticleSerializer, CommentSerializer, FeatureFlagSerializer
from .permissions import IsOwner, IsOwnerOrAdmin, CreateUserPermission, CommentPermissionClass
from django.conf import settings
import requests

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CreateUserPermission]

    def create(self, request, *args, **kwargs):
        # If no users exist, create the first user with the "Owner" role
        if not User.objects.exists():
            request.data['role'] = 'Owner'
        else:
            # If the user is not the first one, use the role from the request data
            role = request.data.get('role', 'Member')
            request.data['role'] = role
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=False, methods=['post'], url_path='generate-content')
    def generate_content(self, request):
        # Only allow Admins or Owners to generate content
        if not request.user.role in ['Admin', 'Owner']:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        feature_flag = FeatureFlag.objects.filter(name='LLM Article Generation').first()
        if feature_flag and not feature_flag.is_enabled:
            return Response({"error": "LLM Article Generation is disabled"}, status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title', '')
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # LLM API call (OpenAI example)
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {settings.OPENAI_API_KEY}'},
            json={
                'model': 'gpt-3.5-turbo',
                'prompt': f"Write a detailed blog post about: {title}",
                'max_tokens': 500
            }
        )

        if response.status_code != 200:
            return Response({"error": "Failed to generate content from LLM"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        content = data.get('choices', [{}])[0].get('text', '').strip()
        return Response({"title": title, "content": content}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        instance = serializer.save()
        feature_flag = FeatureFlag.objects.filter(name='LLM Tags Generation').first()
        if feature_flag and feature_flag.is_enabled:
            response = requests.post(
                'https://api.openai.com/v1/completions',
                headers={'Authorization': f'Bearer {settings.OPENAI_API_KEY}'},
                json={
                    'model': 'gpt-3.5-turbo',
                    'prompt': f"Suggest tags for this article: {instance.title}\n\nContent: {instance.content}",
                    'max_tokens': 50
                }
            )
            if response.status_code == 200:
                data = response.json()
                tags = data.get('choices', [{}])[0].get('text', '').strip()
                instance.tags = tags
                instance.save()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissionClass]

class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsOwner]
