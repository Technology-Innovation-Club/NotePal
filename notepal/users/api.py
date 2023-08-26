from ninja import Form, Router, Schema
from django.contrib.auth.models import User
from ninja.errors import HttpError
from django.utils import timezone
import re

notepal_router = Router()


class SignUp(Schema):
    email: str
    password: str
    repeat_password: str
    


@notepal_router.post("/signup")
def signup(request, signup_details: SignUp = Form(...)):
    username = signup_details.username
    password = signup_details.password
    email = signup_details.email

    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            last_login=timezone.now(),
        )
    except Exception as e:
        raise e


    return user.notepaluser.created_ts


def email_check(email: str) -> bool:
    new_email = email.split("@")
    if new_email[1] == "pau.edu.ng":
        return True
    else:
        return False


# Login can be done through 'accounts/login' and logout through 'accounts/logout'
