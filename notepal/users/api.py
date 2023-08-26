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
    if not signup_validate_required_fields(signup_details):
        return signup_validate_required_fields(signup_details)
    if not validate_signup_details(signup_details):
        return validate_signup_details(signup_details)
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


def signup_validate_required_fields(data):
    errors = {}
    if data.email == "":
        errors["email"] = "Email is required"
    if data.password == "":
        errors["password"] = "Password is required"
    if data.repeat_password == "":
        errors["repeat_password"] = "Repeat password is required"
    if errors:
        raise HttpError(422, message=errors)
    return True

def validate_signup_details(signup_details):
    errors = {}
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', signup_details.email):
        errors["email"] = "Invalid email address"
    if User.objects.filter(email=signup_details.email).exists():
        errors["email"] = "Email is already in use"
    if signup_details.password != signup_details.repeat_password:
        errors['password'] = "Passwords do not match"
    if len(signup_details.password)<8:
        errors['password'] = "Password is too short. It must be at least 8 characters long"
    if errors:
        raise HttpError(422, message=errors)
    return True


# Login can be done through 'accounts/login' and logout through 'accounts/logout'
