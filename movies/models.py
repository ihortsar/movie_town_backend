from datetime import date
from django.db import models

from user.models import CustomUser

# Create your models here.


class Movie(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
