from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from book.models import Book
from .models import Review

# Create your views here.


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if user already reviewed this book
    existing_review = Review.objects.filter(
        user=request.user,
        book=book,
    ).first()

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
