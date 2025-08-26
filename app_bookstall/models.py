from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
