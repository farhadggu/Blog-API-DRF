from codecs import lookup
from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('article', views.ArticleViewSet)

comment_router = routers.NestedDefaultRouter(router, 'article', lookup='article')
comment_router.register('comment', views.CommentViewSet, basename='comment')


urlpatterns = router.urls + comment_router.urls
