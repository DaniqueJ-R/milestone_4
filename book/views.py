from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def books_page(request):
    """ A view to render index page"""

    return render(request, "book/index.html")
