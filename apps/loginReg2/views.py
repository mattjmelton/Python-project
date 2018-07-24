from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def index(request):
    print("in the index method")
    return render(request, "loginReg/index.html")

def create(request):
    print("in the create user method")
    print(request.POST)
    response = ""
    if 'confirm_password' in request.POST:
        response = User.objects.user_validator(request.POST)
    else:
        response = User.objects.login_validator(request.POST)
    if type(response)==int:
        print(response)
        request.session['user_id'] = response
        return redirect('jobs/dashboard')
    else:
        print(response)
        for error in response:
            messages.error(request, error)
        return redirect('/')
    

def logout(request):
    print("in the logout method")
    request.session.clear()
    return redirect('/')
        

