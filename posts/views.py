from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


def toggle_active(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.is_active = not post.is_active
        post.save()

    return redirect('post_detail', pk=pk)