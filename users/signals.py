from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import NotepalUser

@receiver(post_save, sender=User)
def create_notepaluser(sender, instance, created, **kwargs):
    if created:
        notepal_user = NotepalUser(user=instance)
        notepal_user.save()
        


