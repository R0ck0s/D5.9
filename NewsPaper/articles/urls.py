from news.views import NewsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete
from django.urls import path


urlpatterns = [
    path('create/', PostCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name = 'article_delete'),
]