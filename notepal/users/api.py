from ninja import Form, Router, Schema
from django.contrib.auth.models import User

notepal_router = Router()


class SignUp(Schema):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str


@notepal_router.post("/signup")
def signup(request, signup_details: SignUp = Form(...)):
    username = signup_details.username
    password = signup_details.password
    email = signup_details.email
    first_name = signup_details.first_name
    last_name = signup_details.last_name

    if email_check(email):
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        except Exception as e:
            raise e
    else:
        return "Please sign up with your PAU email address"

    return user.notepaluser.created_ts


def email_check(email: str) -> bool:
    new_email = email.split("@")
    if new_email[1] == "pau.edu.ng":
        return True
    else:
        return False


# Login can be done through 'accounts/login' and logout through 'accounts/logout'
