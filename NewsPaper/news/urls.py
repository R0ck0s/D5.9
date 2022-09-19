# from django.urls import path
from .views import NewsList, PostDetail
from django.urls import path, include

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]