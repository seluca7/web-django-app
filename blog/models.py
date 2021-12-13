from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Books(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20)
    book_author = models.CharField(max_length=40, default="")
    year_released = models.IntegerField(default=datetime.now().year)
    avg_rating = models.IntegerField(default=1)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='book.png', upload_to='book_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books-detail', kwargs={'pk': self.pk})


class Review(models.Model):
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'

    ratings = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    title = models.CharField(max_length=100)
    rating = models.IntegerField(choices=ratings, default=1)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})
