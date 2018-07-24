from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job

def index(request):
    print("in the jobs index method")

    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : this_user,
        'joined_job' : Job.objects.filter(job_joined_by=request.session['user_id']),
        'all_unjoined_jobs' : Job.objects.exclude(job_joined_by=request.session['user_id'])
    }

    return render(request,'jobs/index.html',context)

def newjob(request):
    print("in the add jobs method")
    print(request.POST)

    response = Job.objects.job_validator(request.POST)
    print(response)
    if type(response)==int:
        request.session['job_id'] = response
        return redirect('jobs/dashboard')
    else:
        print(response)
        for error in response:
            messages.error(request, error)
        return redirect('jobs/newjob')


    return render(request,'jobs/new.html')
