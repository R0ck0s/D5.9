from django.contrib import admin
from .models import Post, Category, Author, Comment, Subscribers

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
