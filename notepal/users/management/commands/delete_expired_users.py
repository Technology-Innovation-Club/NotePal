from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deletes every user in which their session has expired.'

    def handle(self, *args, **options):
        """
        Deletes every user in which their session has expired.
        """

        # Get all expired sessions
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())

        # Get all users associated with the expired sessions
        expired_users = []
        for session in expired_sessions:
            user_id = session.get_decoded().get('_auth_user_id')
            try:
                user = User.objects.get(pk=user_id)
                expired_users.append(user)
            except User.DoesNotExist:
                continue
            
        # Delete all expired sessions
        for session in expired_sessions:
            session.delete()
        
        # Delete all expired users
        for user in expired_users:
            user.delete()


