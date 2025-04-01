from django.shortcuts import render
from .models import Person

def person(request):
    person = Person.objects.all()