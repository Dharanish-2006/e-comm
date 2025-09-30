from .forms import SignUpForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import LoginView

# def login_page(request):
#     context = { "error":"" }
#     if request.method== "POST":
#         user = authenticate(username= request.POST['username'],password=request.POST['password'])
#         if(user is not None):
#             login(request,user)
#             return redirect('/home/')
#         else:
#             context = { "error":"thappu" }
#     return render(request,'login.html',context)

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
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})