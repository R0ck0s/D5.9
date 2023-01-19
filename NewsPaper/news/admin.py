from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'author', 'post_rating', 'post_date')
    list_filter = ('post_rating', 'post_date')
    search_fields = ('post_title', 'post_text')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
