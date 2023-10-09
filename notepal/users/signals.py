from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import NotepalUser
from django.contrib.auth.signals import user_logged_out

@receiver(post_save, sender=User)
def create_notepaluser(sender, instance, created, **kwargs):
    if created:
        notepal_user = NotepalUser(user=instance)
        notepal_user.save()
        
@receiver(user_logged_out) 
def _user_logged_out(sender, user, request, **kwargs):
    user.delete()

