from .views import NewsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, upgrade_user
from django.urls import path


urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('upgrade/', upgrade_user, name='upgrade'),
]