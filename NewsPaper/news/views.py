from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


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
        if self.request.method == 'POST':
            post_path = self.request.META['PATH_INFO']
            if post_path == '/news/create/':
                post.post_type = 'NW'
            elif post_path == '/articles/create/':
                post.post_type = 'AR'

            return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.change_post')
    template_name = 'update.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def upgrade_user(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')
