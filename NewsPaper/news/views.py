from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .tasks import notify_about_new_post


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
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'


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

            for i in id_categories:
                cat = Category.objects.get(pk=i)
                post.category.add(cat)

            notify_about_new_post(post)



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


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-post_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'post_created_email.html', {'category': category, 'message': message})





