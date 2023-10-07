from django.shortcuts import render


def signup(request):
    title = "| Sign up"
    context = {"title": title}
    return render(request, "signup.html", context)


def login(request):
    title = "| Sign in"
    context = {"title": title}
    return render(request, "login.html", context)


def forgot_password(request):
    title = "| Forgot password"
    context = {"title": title}
    return render(request, "forgotpass.html", context)


def landing_page(request):
    return render(request, "landing_page.html")
