from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = [
           'author',
           'category',
           'post_title',
           'post_text',
       ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('post_title')
        text = cleaned_data.get('post_text')

        if text == title:
            raise ValidationError(
                {'text': 'Текст публикации не должен быть идентичен её названию'}
            )
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user