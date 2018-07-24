from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt


def index(request):
    print("in the index method")
    if 'login' not in request.session:
        request.session['login'] =0
        request.session['user_id'] =0

    return render(request,"loginReg/index.html")

def create(request):
    print("in the create method for the REGISTRATION form")
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
    # send POST data to the model to create users
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        # messages.success(request)
        registered_user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = registered_user.id
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['login'] = 0
        return redirect('/jobs/dashboard')

def process(request):
    print("in the process method for LOGIN")
    print(request.POST)
    print(request.session['user_id'])
    # if 'first_name' not in request.session:
    #     request.session['first_name']
    user_list = User.objects.filter(email=request.POST['email'])
    print(user_list)
       
    errors = User.objects.login_validator(request.POST)
    
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            print("failed password")
        return redirect('/')
    else:
        
        print("password match")
        request.session['first_name']=user_list[0].first_name
        request.session['last_name']=user_list[0].last_name
        request.session['login']= 1
        request.session['user_id']=user_list[0].id
        print(request.session['user_id'])
        # Redirect to the message app's create message method
        return redirect('/jobs/dashboard')
    

def success(request):
    print("in the success method")
    return render(request, "loginReg/success.html")

def logout(request):
    request.session.clear()
    return redirect('/')