from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def verification_pre_save(sender, instance, created, **kwargs):
    if created:
        print("user created")
