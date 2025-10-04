from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, TrackerStatus, TrackerList
from review.models import Review

# Create your views here.
def books_page(request):
    """ A view to render index page"""

    # Get some books for "Books this week"
    featured_books = Book.objects.all()[:6]

    # If user is logged in, get their tracked books
    if request.user.is_authenticated:
        reading_books = TrackerList.objects.filter(
            user=request.user, 
            status=TrackerStatus.READING
        )[:6]
        reading_count = TrackerList.objects.filter(user=request.user, status=TrackerStatus.READING).count()
        completed_count = TrackerList.objects.filter(user=request.user, status=TrackerStatus.COMPLETE).count()
        plan_count = TrackerList.objects.filter(user=request.user, status=TrackerStatus.PLAN_TO).count()

        # Recent reviews from this user
        recent_reviews = Review.objects.filter(user=request.user).order_by('-created_on')[:4]
    else:
        reading_books = None
        reading_count = completed_count = plan_count = 0
        recent_reviews = Review.objects.all().order_by('-created_on')[:4]

    context = {
        'featured_books': featured_books,
        'reading_books': reading_books,
        'reading_count': reading_count,
        'completed_count': completed_count,
        'plan_count': plan_count,
        'recent_reviews': recent_reviews,
    }

    return render(request, 'book/index.html', context)

def my_library(request, slug):
    """ A view to show individual book details """

    book = get_object_or_404(Book, slug=slug)

    context = {
        'book': book,
    }

    return render(request, 'book/my_library.html', context)
