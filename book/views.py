from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect

from .models import Book, TrackerStatus, TrackerList
from review.models import Review
from review.forms import ReviewForm

# Create your views here.


def books_page(request):
    """ A view to render index page"""

    # Get some books for "Books this week"
    featured_books_auth = Book.objects.all().order_by('?')[:6]
    featured_books_unauth = Book.objects.all().order_by('?')[:12]

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
        'featured_books_auth': featured_books_auth,
        'featured_books_unauth': featured_books_unauth,
        'reading_books': reading_books,
        'reading_count': reading_count,
        'completed_count': completed_count,
        'plan_count': plan_count,
        'recent_reviews': recent_reviews,
    }

    return render(request, 'book/index.html', context)


def book_details(request, slug):
    """ A view to show individual book details """

    book = get_object_or_404(Book, slug=slug)  
    book_reviews = Review.objects.filter(book=book).order_by('-created_on')[:4]
    other_books = Book.objects.exclude(id=book.id).order_by('?')[:3]
    avg_rating = book_reviews.aggregate(Avg('star_rating'))['star_rating__avg']

    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, book=book).first()
        user_completed = TrackerList.objects.filter(
            user=request.user, 
            book=book, 
            status=TrackerStatus.COMPLETE
        ).exists()

    # Get existing review if user is authenticated
    user_review = None
    user_completed = False

    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            user=request.user,
            book=book
        ).first()

    # Initialize form with existing review data
    review_form = ReviewForm(instance=user_review)

    context = {
        'book': book,
        'book_reviews': book_reviews,
        'other_books': other_books,
        'avg_rating': avg_rating,
        'review_count': book_reviews.count(),
        'user_review': user_review,
        'user_completed': user_completed,
        'review_form': review_form,
    }

    return render(request, 'book/book_details.html', context)

@login_required
def add_or_update_tracker(request, book_id):
    """Add book to tracker OR update status if already exists"""

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        status = request.POST.get('status')

        # Try to get existing tracker
        tracker, created = TrackerList.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'status': status} if status else {} #prevents server error
        )

        if created:
            messages.success(request, f"'{book.title}' added to your library!")
        else:
            # Already exists, update the status
            tracker.status = int(status)
            tracker.save()
            messages.success(request, f"'{book.title}' moved to {tracker.get_status_display()} list!")

        return redirect('book_details', slug=book.slug)

    return redirect('book_details', slug=book.slug)


@login_required
def my_library(request):
    """
    Display the logged in user's Complete, 
    Plan to read, and Reading book lists.
    """

    all_books = TrackerList.objects.filter(
        user=request.user)
    reading_books = TrackerList.objects.filter(
        user=request.user, status=TrackerStatus.READING).order_by('-added_on')
    plan_books = TrackerList.objects.filter(
        user=request.user, status=TrackerStatus.PLAN_TO).order_by('-added_on')
    completed_books = TrackerList.objects.filter(
        user=request.user, 
        status=TrackerStatus.COMPLETE
    ).select_related('book').prefetch_related('book__reviews').order_by('-added_on')

    for book in completed_books:
        book.user_review = book.book.reviews.filter(user=request.user).first()

    context = {
        'reading_books': reading_books,
        'completed_books': completed_books,
        'plan_books': plan_books,
        'all_books': all_books,
    }

    return render(request, 'book/my_library.html', context)


@login_required
def edit_tracker(request, tracker_id):
    tracker = get_object_or_404(TrackerList, id=tracker_id, user=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if not new_status:
            messages.error(request, "No status selected. Please try again.")
            return redirect('my_library')

        tracker.status = int(new_status)
        tracker.save()
        messages.success(
            request,
            (
                f"'{tracker.book.title}' was moved to "
                f"{tracker.get_status_display()} in your library."
            )
        )
    return redirect('my_library')


@login_required
def delete_tracker(request, tracker_id):
    tracker = get_object_or_404(TrackerList, id=tracker_id, user=request.user)
    if request.method == 'POST':
        title = tracker.book.title
        tracker.delete()
        messages.success(request, f"'{title}' was deleted from your library.")
    return redirect('my_library')
