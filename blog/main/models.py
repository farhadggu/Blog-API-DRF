from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True    


class Category(TimeStamp):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='media')

    class Meta(TimeStamp.Meta):
        ordering = ['-created']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])
    
    def get_absolute_url(self):
        return reverse("article:category-list", args=[self.slug])

    def image_thumbnail(self):
        return format_html('<img src="{}" width=100px />'.format(self.image.url))
    image_thumbnail.short_description = 'Image'


class Article(TimeStamp):
    STATUS = (
        ('p', 'Published'),
        ('d', 'Draft'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media')
    status = models.CharField(choices=STATUS, max_length=1)

    class Meta(TimeStamp.Meta):
        ordering = ['-created']

    def __str__(self):
        return f'{self.title} - {self.category.title}'

    def get_absolute_url(self):
        return reverse("article:article-detail", args=[self.slug])

    def image_thumbnail(self):
        return format_html('<img src="{}" width=100px />'.format(self.image.url))
    image_thumbnail.short_description = 'Image'


class Comment(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta(TimeStamp.Meta):
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} - {self.comment[:10]}'

    