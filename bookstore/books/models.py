from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.title


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_books = models.ManyToManyField(Book, related_name="favorited_by")
    already_read = models.ManyToManyField(Book, related_name="read_by")

    def __str__(self):
        return self.name
