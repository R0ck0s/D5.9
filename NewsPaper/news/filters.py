from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author
from django import forms


class PostFilter(FilterSet):

    title_search = CharFilter(
        field_name='post_title',
        label = 'Название статьи:',
        lookup_expr = 'icontains'
    )

    author_search = ModelChoiceFilter(
        label = 'Автор',
        field_name = 'author_id',
        queryset=Author.objects.all(),
        empty_label='Все авторы',
    )

    post_date__gt = DateFilter(
        field_name='post_date',
        label='Позже чем',
        widget=forms.DateInput(
            attrs={
                'type':'date'
            }
        ),
        lookup_expr='date__gte'
    )
