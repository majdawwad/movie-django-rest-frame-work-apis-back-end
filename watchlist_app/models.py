from django.db import models
from django.core import validators
from django.contrib.auth import models


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    avg_ratings = models.FloatField(default=0)
    number_ratings = models.IntegerField(default=0)
    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    review_user = models.ForeignKey(models.User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(
        WatchList, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return str(self.rating) + " - " + self.watchlist.title + " - " + str(self.review_user)
