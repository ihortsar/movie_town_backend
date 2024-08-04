from datetime import date
from django.db import models

from user.models import CustomUser

# Create your models here.


class Movie(models.Model):
    GENRE_OPTIONS = [
        ("Nature", "Nature"),
        ("Cities", "Cities"),
        ("Sport", "Sport"),
        ("Relationship", "Relationship"),
    ]

    ACCESS_OPTIONS = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thumbnail_file = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_OPTIONS, default="nature")
    access = models.CharField(max_length=10, choices=ACCESS_OPTIONS, default="private")

    def __str__(self):
        return self.title
    
    
