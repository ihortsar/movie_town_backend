import os
from django.dispatch import receiver

from .tasks import convert_480p
from .models import Movie
from django.db.models.signals import post_save, post_delete
import django_rq


@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    print("video saved")
    if created:
        queue = django_rq.get_queue("default", autocommit=True)
        queue.enqueue(convert_480p, instance.video_file.path)


"""deletes file from filesystem when corresponding 'Video' object is deleted"""


@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
