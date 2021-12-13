from django.urls import path
from . import views
from users import views as user_views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView,\
    ReviewListView, ReviewCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView
from django.conf import settings
from django.conf.urls.static import static, serve

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('books/<int:pk>/', PostDetailView.as_view(), name='books-detail'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('review/<int:pk>/update', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('books/<int:pk>/update/', PostUpdateView.as_view(), name='books-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('books/<int:pk>/delete/', PostDeleteView.as_view(), name='books-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('books/new/', PostCreateView.as_view(), name='books-create'),
    path('register/', user_views.register, name='register'),
    path('books/<int:pk>/see_reviews/', ReviewListView.as_view(), name='book-reviews'),
    path('books/<int:pk>/add_review/', ReviewCreateView.as_view(), name='add-review'),
    path('books/see_reviews/', ReviewListView.as_view(), name='book-review'),
    path('about/', views.about, name='blog-about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

