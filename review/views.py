from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from book.models import Book, TrackerList, TrackerStatus
from .models import Review

# Create your views here.


@login_required
def add_review(request, book_id):
    """
    Stores a single review in relaion to:
    """

    book = get_object_or_404(Book, id=book_id)

    # Check if user already reviewed this book
    existing_review = Review.objects.filter(
        user=request.user,
        book=book,
    ).first()

    user_completed = TrackerList.objects.filter(
        user=request.user,
        book=book,
        status=TrackerStatus.COMPLETE
    ).exists()
    
    if not user_completed:
        messages.error(request, "You must complete this book before leaving a review.")
        return redirect('book_details', slug=book.slug)

    if request.method == 'POST':
        review_title = request.POST.get('review_title')
        review_body = request.POST.get('review_body')
        star_rating = request.POST.get('star_rating')

        if existing_review:
            # Update existing review
            existing_review.review_title = review_title
            existing_review.review_body = review_body
            existing_review.star_rating = star_rating
            existing_review.save()
            messages.success(request, "Review updated!")
        else:
            # Create new review
            Review.objects.create(
                user=request.user,
                book=book,
                review_title=review_title,
                review_body=review_body,
                star_rating=star_rating
            )
            messages.success(request, "Review added!")

        return redirect('book_details', slug=book.slug)


@login_required
def delete_review(request, review_id):
    """
    Deletes a single review.
    """

    # Fetch the review, 404 if not found
    try:
        existing_review = Review.objects.get(review_id=review_id)
    except Review.DoesNotExist:
        messages.error(request, "This review has already been removed.")
        # You can redirect to any fallback page if the review is gone
        return redirect('my_library')

    book = existing_review.book

    # Only allow the review owner to delete it
    if existing_review.user != request.user:
        messages.error(request, "You do not have permission to delete this review.")
        return redirect('book_details', slug=book.slug)

    if request.method == 'POST':
        review_title = existing_review.review_title
        existing_review.delete()
        messages.success(request, f"'{review_title}' was deleted from your account.")
        return redirect('book_details', slug=book.slug)

    # If not a POST request, just redirect back to the user's library
    return redirect('book_details', slug=book.slug)
