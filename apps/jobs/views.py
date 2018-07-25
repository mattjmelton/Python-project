from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job

# Create your views here.
def index(request):
    print("I'm in the index method.")
    # if 'user_id' != request.session:
    #     redirect('/')

    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': this_user,
        'joined_job' : Job.objects.filter(job_joined_by=request.session['user_id']),
        'all_unjoined_jobs' : Job.objects.exclude(job_joined_by=request.session['user_id']),
        'all_jobs' : Job.objects.all()
    }
    return render(request,"jobs/index.html", context)

def new(request):
    print("I'm in the new method")
    return render(request,"jobs/new.html")

def addjob(request):
    print("I'm in the create a TRIP method.")
    print(request.POST)
    errors = Job.objects.job_validator(request.POST)
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:
        job = Job.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                location = request.POST['location'],
                job_created_by = User.objects.get(id=request.session['user_id'])
        )
            # messages.success(request, "Successfully added a user.")
        
        # this_user = User.objects.get(id=request.session['user_id'])
        # print(this_user)
        # this_user.joined_job.add(job)
        # job.save()
        return redirect('/jobs/dashboard')

def show(request, job_id):
    print("in the Show job method")
    job = Job.objects.get(id=job_id)
    context = {
        'job' : job,
        'job_joined_by' : User.objects.filter(joined_job=job_id).exclude(id=job.job_created_by.id)
    }
    return render(request, "jobs/show.html", context)

# Create a relationship between the user and the trip to be joined
def join(request, job_id):
    print("in the Join JOB method")
    
    join_job = Job.objects.get(id=job_id)
    print(join_job)
    this_user = User.objects.get(id=request.session['user_id'])
    print(this_user)
    
    this_user.joined_job.add(join_job)
    
    return redirect('/jobs/dashboard')


def edit(request, job_id):
    print("in the Edit job method")
    context = {
        'job' : Job.objects.get(id=job_id)
    }
    return render(request, "jobs/edit.html", context)

def update(request):
    print("in the Update job method")
    print(request.POST)
    job_id = request.POST['job_id']
    errors = Job.objects.job_validator(request.POST)
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        jid = '/edit/'+ str(job_id)
        return redirect(jid)
    else:
        job_to_update = Job.objects.get(id=request.POST['job_id'])
        job_to_update.title = request.POST['title']
        job_to_update.description = request.POST['description']
        job_to_update.location = request.POST['location']
        job_to_update.save()
        messages.success(request, "Successfully added a user.")

        return redirect('/jobs/dashboard')

# Delete the relationship between the user and the joined trip
def cancel(request, job_id):
    print("in the cancel job method")

    join_job = Job.objects.get(id=job_id)
    print(join_job)
    this_user = User.objects.get(id=request.session['user_id'])
    print(this_user)
    
    this_user.joined_job.remove(join_job)
    return redirect('/jobs/dashboard')


def destroy(request, job_id):
    print("I'm in Destroy job method")
    # Delete the trip whose Id came into the method
    Job.objects.get(id=job_id).delete()

    return redirect('/jobs/dashboard')



