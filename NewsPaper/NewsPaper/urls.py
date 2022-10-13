from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('articles/', include('articles.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('news.urls')),

]
