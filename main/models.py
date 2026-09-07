from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def count_books(self):
        return len(self.book_set.filter(published=True))


class Book(models.Model):
    title = models.CharField(max_length=255)
    introduction = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    category = models.ForeignKey (Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    text = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey (Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return self.text
