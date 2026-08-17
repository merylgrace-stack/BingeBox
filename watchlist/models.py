from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Media(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('tv_show', 'TV Show'),
    ]

    STATUS_CHOICES = [
        ('unwatched', 'Unwatched'),
        ('watched', 'Watched'),
    ]

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='watchlist',
    )

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10,
                               choices=STATUS_CHOICES,
                                 default='unwatched'
    )
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title