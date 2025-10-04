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
        completed_count = TrackerList.objects.filter(user=request.user, status=TrackerStatus.READING).count()
        plan_count = TrackerList.objects.filter(user=request.user, status=TrackerStatus.READING).count()

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

# def post_detail(request, slug):
#     """
#     Display an individual :model:`blog.Post`.

#     **Context**

#     ``post``
#         An instance of :model:`blog.Post`.
#     ``comments``
#         All approved comments related to the post.
#     ``comment_count``
#         A count of approved comments related to the post.
#     ``comment_form``
#         An instance of :form:`blog.CommentForm`

#     **Template:**

#     :template:`blog/post_detail.html`
#     """

#     queryset = Post.objects.filter(status=1)
#     post = get_object_or_404(queryset, slug=slug)
#     review = post.comments.all().order_by("-created_on")
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
