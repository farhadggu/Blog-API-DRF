from django.contrib import admin
from .models import Category, Article, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image_thumbnail',]
    prepopulated_fields = {'slug':('title',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image_thumbnail',]
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)