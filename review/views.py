from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from book.models import Book, TrackerList, TrackerStatus
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, book_id):
    """
    Add or update a review for a book
    """
    book = get_object_or_404(Book, id=book_id)

    # Check if user has completed the book
    user_completed = TrackerList.objects.filter(
        user=request.user, book=book, status=TrackerStatus.COMPLETE
    ).exists()

    if not user_completed:
        messages.error(
            request,
            "You must complete this book before leaving a review.",
        )
        return redirect("book_details", slug=book.slug)

    # Check if user already reviewed this book
    existing_review = Review.objects.filter(
        user=request.user,
        book=book,
    ).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()

            if existing_review:
                messages.success(request, "Review updated!")
            else:
                messages.success(request, "Review added!")

            return redirect("book_details", slug=book.slug)
        else:
            message = "Please correct the errors in your review."
            messages.error(request, message)
            return redirect("book_details", slug=book.slug)

    return redirect("book_details", slug=book.slug)


@login_required
def delete_review(request, id):
    """
    Delete a review
    """
    review = get_object_or_404(Review, id=id)
    book = review.book

    # Only allow the review owner to delete it
    if review.user != request.user:
        message = "You do not have permission to delete this review."
        messages.error(request, message)
        return redirect("book_details", slug=book.slug)

    if request.method == "POST":
        review_title = review.review_title
        review.delete()
        message = f"'{review_title}' was deleted from your account."
        messages.success(request, message)
        return redirect("book_details", slug=book.slug)

    # If not a POST request, redirect back
    return redirect("book_details", slug=book.slug)
