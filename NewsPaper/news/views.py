from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscribers, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



class NewsList(ListView):
    model = Post
    ordering = 'post_title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.add_post')
    template_name = 'create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        today_date = datetime.now().date()
        post_count = Post.objects.filter(author_id = post.author, post_date__gte=today_date).count()
        print(post_count)
        if post_count < 3:
            if self.request.method == 'POST':
                post_path = self.request.META['PATH_INFO']
                if post_path == '/news/create/':
                    post.post_type = 'NW'
                elif post_path == '/articles/create/':
                    post.post_type = 'AR'
                post.save()

            id_categories = self.request.POST.getlist('category')
            id_post = Post.objects.last()
            subscribers_mail_sent(id_categories, id_post)

            return super().form_valid(form)

        else:
            print('Вы привысили лимит на написание новостей. Не больше 3 в сутки')

        return HttpResponseRedirect('/news/')


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.change_post')
    template_name = 'update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


# Добавление пользователя в группу авторов
@login_required
def upgrade_user(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user_id = user.id)
    return redirect('/news/')


# Рассылка новости пользователям, подписавшимся на категорию
def subscribers_mail_sent(cat_id, post_id):

    for cat in cat_id:
        emails = User.objects.filter(subscribers__category_id=cat).values('email').distinct()
        email_list = [item['email'] for item in emails]
        cat_name = Category.objects.get(pk = cat)

        html_content = render_to_string(
            'news_created.html',
            {
                'post_id': post_id,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Появилась новость в разделе {cat_name}',
            from_email='skilltests77@yandex.ru',
            to=email_list )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


# Подписка на категорию
@login_required()
def subscribe(request, i):
    s_user = User.objects.get(username=request.user)

    if s_user:
        Subscribers.objects.create(category_id = i, user_id = s_user.id)

    return redirect('/news/')


