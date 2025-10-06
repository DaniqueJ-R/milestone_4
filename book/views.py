from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from django.http import HttpResponse

from .models import Book, TrackerStatus, TrackerList
from review.models import Review

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
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comments``
        All approved comments related to the post.
    ``comment_count``
        A count of approved comments related to the post.
    ``comment_form``
        An instance of :form:`blog.CommentForm`

    **Template:**

    :template:`blog/post_detail.html`
    """
    """ A view to show individual book details """

    queryset = Book.objects.all()
    book = get_object_or_404(queryset, slug=slug)  
    book_reviews = Review.objects.filter(book=book).order_by('-created_on')[:4]
    other_books = Book.objects.exclude(id=book.id).order_by('?')[:3]
    avg_rating = book_reviews.aggregate(Avg('star_rating'))['star_rating__avg']
    # This returns None if no reviews exist

    context = {
        'book': book,
        'book_reviews': book_reviews,
        'other_books': other_books,
        'avg_rating': avg_rating,
        'review_count': book_reviews.count(),
    }

    return render(request, 'book/book-details.html', context)


def my_library(request):

    return render(request, 'book/my-library.html')
# def post_detail(request, slug):

#     queryset = Post.objects.filter(status=1)
#     post = get_object_or_404(queryset, slug=slug)
#     comments = post.comments.all().order_by("-created_on")
#     comment_count = post.comments.filter(approved=True).count()
#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             messages.add_message(
#                 request, messages.SUCCESS,
#                 'Comment submitted and awaiting approval'
#             )
#     comment_form = CommentForm()

#     return render(
#         request,
#         "blog/post_detail.html",
#         {
#             "post": post,
#             "comments": comments,
#             "comment_count": comment_count,
#             "comment_form": comment_form,
#         },
#     )
