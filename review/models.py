# from django.db import models
# from django.contrib.auth.models import User
# from book.models import Book

# # Create your models here.


# class Review(models.Model):
#     """
#     Stores a single review in relaion to:
#     :model:'auth.user:' and :model:'books:'.
#     """
#     STAR_RATING = (
#         (0, "0 stars"),
#         (1, "1 stars"),
#         (2, "2 stars"),
#         (3, "3 stars"),
#         (4, "4 stars"),
#         (5, "5 stars"),
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="reviews")
#     book = models.ForeignKey(
#         Book, on_delete=models.CASCADE, related_name="reviews")
#     review_title = models.CharField(max_length=300)
#     review_body = models.TextField()
#     star_rating = models.IntegerField(choices=STAR_RATING, default=1)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Review of {self.book.title} by {self.user.username}"
