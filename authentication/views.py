from .forms import SignUpForm
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings

class CustomLoginView(LoginView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_navbar"] = False
        return context
    template_name = "login.html"

def LogoutUser(request):
    logout(request)
    return(redirect('/'))

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.core.mail import send_mail

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.email:
                send_mail(
                    subject="Welcome to E-Comm 🎉",
                    message=(
                        f"Hi {user.username},\n\n"
                        "Welcome to E-Comm!\n\n"
                        "You can now place orders, track them, and enjoy shopping.\n\n"
                        "Happy Shopping 🛒\n"
                        "CARTSY Team"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )

            return redirect("home")
    else:
        form = SignUpForm()

    return render(
        request,
        "signup.html",
        {
            "form": form,
            "show_navbar": False,
        }
    )
