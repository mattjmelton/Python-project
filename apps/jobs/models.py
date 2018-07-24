from django.db import models
from ..loginReg.models import User


class JobManager(models.Manager):
    def job_validator(self, postData):
        print("in the job validator")
        print(postData)
        
        errors = {}
        if not len(postData['title']):
            errors["title"] = "Please enter a title."
        if len(postData['title']) < 4:
            errors['title'] = "Please enter a title with 4 or more characters."
        if not len(postData['description']):
            errors["description"] = "Please enter a description."
        if len(postData['description']) < 11:
            errors['description'] = "Please enter a description with more than 10 characters."
        if not len(postData['location']):
            errors["location"] = "Please enter a location"
        return errors


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job_created_by = models.ForeignKey(User, related_name="created_job")
    job_joined_by = models.ManyToManyField(User, related_name="joined_job")

    objects = JobManager()
    