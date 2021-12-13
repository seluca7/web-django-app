from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Avg
from .models import Post, Books, Review
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


def home(request):
    context = {
        'books': Books.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Books
    template_name = 'blog/home.html'
    context_object_name = 'books'
    ordering = ['title']
    paginate_by = 2


class UserPostListView(ListView):
    model = Review
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Books


class ReviewDetailView(DetailView):
    model = Review


class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'blog/see_reviews.html'
    paginate_by = 5

    def get_queryset(self):
        book = get_object_or_404(Books, id=self.kwargs.get('pk'))
        return Review.objects.filter(book=book)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        book = get_object_or_404(Books, id=self.kwargs.get('pk'))
        avg = list(Review.objects.filter(book=book).aggregate(Avg('rating')).values())[0]
        context['average_rt'] = avg
        context['book_title'] = book.title
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Books
    fields = ['title', 'genre', 'book_author', 'year_released', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['title', 'rating', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.book = get_object_or_404(Books, id=self.kwargs.get('pk'))
        return super().form_valid(form)
# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Books
    fields = ['title', 'genre', 'book_author', 'year_released', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    fields = ['title', 'rating', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Books
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
