from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import NotepalUser


@receiver(post_save, sender=User)
def create_notepaluser(sender, instance, created, **kwargs):
    if created:
        NotepalUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_notepaluser(sender, instance, **kwargs):
    instance.notepaluser.save()
