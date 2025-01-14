from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import UserViewSet, ArticleViewSet, CommentViewSet, FeatureFlagViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('articles', ArticleViewSet)
router.register('comments', CommentViewSet)
router.register('feature-flags', FeatureFlagViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
