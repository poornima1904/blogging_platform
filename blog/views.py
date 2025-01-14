from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Article, Comment, FeatureFlag
from .serializers import UserSerializer, ArticleSerializer, CommentSerializer, FeatureFlagSerializer
from .permissions import IsOwner, IsOwnerOrAdmin, CreateUserPermission, CommentPermissionClass
from django.conf import settings
from .service import *
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


    def perform_create(self, serializer):
        """
        check if feature flags are enabled for LLM Article Content & Tag generation.
        If enabled, use the LLM to generate content and tags; otherwise, honor the request data.
        """

        request_data = self.request.data.copy()
        title = request_data.get('title', '')
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get feature flags
        llm_article_flag = FeatureFlag.objects.filter(name='LLM Article Generation', is_enabled=True).exists()
        llm_tags_flag = FeatureFlag.objects.filter(name='LLM Tags Generation', is_enabled=True).exists()

        # Check if LLM Article Generation flag is enabled
        if llm_article_flag:
            # Call a function to generate the article content using an LLM service
            generated_content = generate_article_content(title)  # Function to generate content via LLM
            request_data['content'] = generated_content

        # Check if LLM Tags Generation flag is enabled
        if llm_tags_flag:
            # Call a function to generate tags using an LLM service
            generated_tags = generate_tags(title)  # Function to generate tags via LLM
            request_data['tags'] = generated_tags
        else:
            # If LLM Tag Generation is not enabled, use the tags provided in the request
            tags = request_data.get('tags', '')
            request_data['tags'] = tags  # Ensure that 'tags' are used from the request

        # Save the article with the potentially generated content and tags
        request_data.pop('author')
        serializer.save(author=self.request.user, **request_data)

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle the dynamic content and tag generation.
        """
        # Get the serializer instance to validate and save data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Perform the create operation (which will handle content and tag generation)
        self.perform_create(serializer)
        
        # Return the response with the article data and status
        return Response({
            'article': ArticleSerializer(instance=serializer.instance).data
        }, status=status.HTTP_201_CREATED)

        

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissionClass]

class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsOwner]
