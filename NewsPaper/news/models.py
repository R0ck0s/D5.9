from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

class Author(models.Model):
    author_rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rate = self.post_set.all().aggregate(post_sum = Sum('post_rating') * 3)['post_sum']
        self_comm_rate = self.user.comment_set.all().aggregate(self_comm_sum = Sum('comm_rating'))['self_comm_sum']
        total_comm_rate = self.post_set.all().aggregate(Sum('comment__comm_rating'))['comment__comm_rating__sum']
        own_post_rate = self.user.comment_set.all().filter(post__author_id = self.id).aggregate(Sum('comm_rating'))['comm_rating__sum']
        self.author_rating = posts_rate + self_comm_rate + total_comm_rate - own_post_rate
        self.save()
    def __str__(self):
        return f'{self.user.username}'

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.category_name}'

class Post(models.Model):
    news = 'NW'
    article = 'AR'

    TYPE_CHOICES = [
        (article, 'Article'),
        (news, 'News')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    post_date = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'

    def __str__(self):
        return f'{self.post_title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comm_text = models.TextField()
    comm_date = models.DateTimeField(auto_now_add=True)
    comm_rating = models.FloatField(default=0.0)

    def like(self):
        self.comm_rating += 1
        self.save()

    def dislike(self):
        self.comm_rating -= 1
        self.save()
