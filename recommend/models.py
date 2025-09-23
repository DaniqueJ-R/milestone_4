# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.


# class Recommend(models.Model):
#     """
#     Stores a single recommendation in relaion to :model:'auth.user:'.
#     """
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="recommendations")
#     books = models.ManyToManyField("Book", related_name="recommendations")
#     genres = models.ManyToManyField("Genre", related_name="recommendations")
#     created_on = models.DateTimeField(auto_now_add=True)
#     # for tracking/debugging
#     updated_on = models.DateTimeField(auto_now=True)
#     # for tracking/debugging

#     def __str__(self):
#         return f"Recommendations for {self.user.username}"
