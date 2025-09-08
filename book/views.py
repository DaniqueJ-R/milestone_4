from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def books_page(request):
    return HttpResponse("I LOVE BOOKS!")
