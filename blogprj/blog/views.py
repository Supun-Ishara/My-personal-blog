from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# posts = [
#     {
#         "author": "Supun Ishara",
#         "title": "Blog post 1",
#         "content": "My first blog",
#         "date_posted": "7th August, 2021"
#     },
#     {
#         "author": "Kasun Jamara",
#         "title": "Blog post 2",
#         "content": "His first blog",
#         "date_posted": "8th August, 2024"
#     }
# ]

# def home(request):
#     context = {
#         "posts": Post.objects.all()
#     }
#     return render(request, "blog/home.html", context)

def about(request):
    return render(request, "blog/about.html", {"title": "About Page"})

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def from_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False