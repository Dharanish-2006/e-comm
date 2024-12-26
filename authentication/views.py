from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

def login_page(request):
    context = { "error":"" }
    if request.method== "POST":
        user = authenticate(username= request.POST['username'],password=request.POST['password'])
        print(user)
        if(user is not None):
            login(request,user)
            return redirect('/home/')
        else:
            context = { "error":"thappu" }

    return render(request,'login.html',context)
def LogoutUser(request):
    logout(request)
    return(redirect('/'))

