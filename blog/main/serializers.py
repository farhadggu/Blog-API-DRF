from rest_framework import serializers
from .models import Category, Article, Comment


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class CategorySerializer(serializers.ModelSerializer):
    parent = ParentSerializer()
    class Meta:
        model = Category
        fields = ['id', 'parent', 'title', 'slug', 'image']


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['parent', 'title', 'slug', 'image']    

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Article
        fields = ['id', 'category', 'title', 'slug', 'description', 'image', 'status']


class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['category', 'title', 'slug', 'description', 'image', 'status']

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment']    


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

    def create(self, validated_data):
        user_id = self.context['user_id']
        article_id = self.context['article_id']
        return Comment.objects.create(user_id=user_id, article_id=article_id, **self.validated_data)

    
