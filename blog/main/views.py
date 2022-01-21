from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CategorySerializer,
    CreateCategorySerializer,
    ArticleSerializer,
    CreateArticleSerializer,
    CommentSerializer,
    CreateCommentSerializer
)
from .models import Category, Article, Comment


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategorySerializer
        return CreateCategorySerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleSerializer
        return CreateArticleSerializer


class CommentViewSet(ModelViewSet):
    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_pk'])

    def get_serializer_context(self):
        return {'user_id':self.request.user.id, 'article_id':self.kwargs['article_pk']}
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        return CreateCommentSerializer