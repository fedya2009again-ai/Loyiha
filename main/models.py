from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Categoriya")

    def __str__(self):
        return self.name

    def count_books(self):
        return len(self.book_set.filter(published=True))

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Kitob nomi")
    introduction = models.TextField(null=True, blank=True, verbose_name="Muqaddima")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    image = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name="Rasmi")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Chiqgan vaqti")
    updated = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    published = models.BooleanField(default=True, verbose_name="Saytga chiqarish")
    category = models.ForeignKey (Category, on_delete=models.CASCADE, verbose_name="Categoriya")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"

class Comment(models.Model):
    text = models.CharField(max_length=500, verbose_name="Matni")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Chiqgan vaqti")
    book = models.ForeignKey (Book, on_delete=models.CASCADE, verbose_name="Kitob")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Foydalanuvchi")

    def _str_(self):
        return self.text

    class Meta:
        ordering = ('-created',)
        verbose_name = "Komentariya"
        verbose_name_plural = "Komentariyalar"
