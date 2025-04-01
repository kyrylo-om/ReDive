from django.db import models

class Person(models.Model):
    name=models.TextField(max_length=75)
    trophy = models.IntegerField()
    date = models.TextField(max_length=75)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name}"
