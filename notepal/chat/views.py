from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat(request):
    user_email = request.user.email
    context = {
        'user_email': user_email,
    }
    return render(request, "chat.html", context)

