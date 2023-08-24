from django.shortcuts import render


def signup(request):
    title = "Sign up"
    context = {'title': title}
    return render(request, "signup.html", context)


def login(request):
    return render(request, "login.html")


def chat(request):
    return render(request, "chat.html")


def landing_page(request):
    return render(request, "landing_page.html")
