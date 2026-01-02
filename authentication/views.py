from .forms import SignUpForm
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail

class CustomLoginView(LoginView):
    template_name = "login.html"

def LogoutUser(request):
    logout(request)
    return(redirect('/'))

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                subject="Welcome to E-Comm 🎉",
                message=(
                    f"Hi {user.username},\n\n"
                    "Welcome to E-Comm!\n\n"
                    "You can now place orders, track them, and enjoy shopping.\n\n"
                    "Happy Shopping 🛒\n"
                    "E-Comm Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})