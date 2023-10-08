from ninja import Schema
from ninja.errors import HttpError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class LoginSchema(Schema):
    email: str
    password: str


def login_validate_required_fields(data):
    errors = {}
    if data.email == "":
        errors["email"] = "Email is required"
    if data.password == "":
        errors["password"] = "Password is required"
    if errors:
        raise HttpError(422, message=errors)
    return True


def login_validate(data):
    error = {}
    if User.objects.filter(email=data.email).exists():
        user = User.objects.get(email=data.email)
    else:
        error["Authentication error"] = "Wrong credentials"
        raise HttpError(401, message=error)
    if not user.is_active:
        error["Authentication error"] = "User is not active"
        raise HttpError(401, message=error)
    else:
        return True
