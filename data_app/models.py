from django.db import models

class History(models.Model):
    name = models.TextField(max_length=75)

    def __str__(self):
        return f'{self.name}'
class Person(models.Model):
    foreign_key = models.ForeignKey(History, on_delete=models.CASCADE)
    name=models.TextField(max_length=75)
    trophy = models.IntegerField()
    date = models.TextField(max_length=75)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name}"
