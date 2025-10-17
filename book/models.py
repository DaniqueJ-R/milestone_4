from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.


class Book(models.Model):
    """
    Stand alone model to get book data from API or Database.
    """
    title = models.CharField(max_length=250)
    book_id = models.CharField(max_length=250, unique=True)
    author = models.CharField(max_length=250)
    link = models.URLField(max_length=250, unique=True)
    cover_image = models.ImageField(
        upload_to='book_covers/', null=True, blank=True
    )
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    published = models.DateField()
    genre = models.ManyToManyField("Genre", related_name="genre")
    created_on = models.DateTimeField(auto_now_add=True)
    # for tracking/debugging
    updated_on = models.DateTimeField(auto_now=True)
    # for tracking/debugging

    def __str__(self):
        return f"Book Title: {self.title}"


class Genre(models.Model):
    """
    Stand-alone class that stores a single
    category/genre from the API or database.
    """
    name = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(default=timezone.now)
    # for tracking/debugging
    updated_on = models.DateTimeField(default=timezone.now)
    # for tracking/debugging

    class Meta:
        ordering = ["name"]  # keeps genres alphabetized

    def __str__(self):
        return self.name


class TrackerStatus(models.IntegerChoices):
    """
    Options for Tracker status in relaion to :model:'tracker.status:'.
    """
    READING = 0, "Reading"
    COMPLETE = 1, "Completed"
    PLAN_TO = 2, "Plan to read"


class TrackerList(models.Model):
    """
    Stores a single tracking shelf in relaion to :model:'auth.user:'.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="trackers")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="trackers")
    status = models.IntegerField(
        choices=TrackerStatus.choices,
        default=TrackerStatus.READING
    )
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "book")  # prevents duplicates
        ordering = ["-updated_on"]  # most recently updated first

    def last_updates(self):
        how_many = now() - self.updated_on
        return f"{how_many.days} days ago"
    
