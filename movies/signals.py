import os
from django.dispatch import receiver
from .tasks import (
    convert_1080p,
    convert_480p,
    convert_720p,
    convert_path,
    create_thumbnail,
)
from .models import Movie
from django.db.models.signals import post_save, post_delete
from django.conf import settings
import django_rq


@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        if not instance.thumbnail_file.name:
            thumbnail_path = create_thumbnail(instance.video_file.path)
            instance.thumbnail_file.name = thumbnail_path[
                len(settings.MEDIA_ROOT) + 1 :
            ]
            instance.save()
    queue = django_rq.get_queue("default", autocommit=True)
    queue.enqueue(convert_720p, instance.video_file.path)
    queue.enqueue(convert_1080p, instance.video_file.path)
    queue.enqueue(convert_480p, instance.video_file.path)


"""deletes file from filesystem when corresponding 'Video' object is deleted"""


@receiver(post_delete, sender=Movie)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        path_720p = convert_path(instance.video_file.path, "720p")
        path_480p = convert_path(instance.video_file.path, "480p")
        path_1080p = convert_path(instance.video_file.path, "1080p")

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            os.remove(instance.thumbnail_file.path)
            if os.path.isfile(path_720p):
                os.remove(path_720p)
            if os.path.isfile(path_480p):
                os.remove(path_480p)
            if os.path.isfile(path_1080p):
                os.remove(path_1080p)
