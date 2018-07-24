from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        # validate first name
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name needs to be at least 2 characters."
        # validate last name
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name needs to be at least 2 characters."
        # validate email
        if len(postData['email']) < 1:
            errors['email'] = "Email needs to be in a valid format."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email needs to be in a valid format."
        elif User.objects.filter(email=postData['email']):  
            errors['email'] = "This email has already been registered."
        # validate password
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords did not match."

        return errors

    def login_validator(self, postData):
        errors = {}
        user_list = User.objects.filter(email=postData['email'])
        # validate email
        if len(postData['email']) < 1:
            errors['email'] = "Email needs to be in a valid format."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email needs to be in a valid format."
        elif not user_list:  
            errors['email'] = "This email has not been registered."
        # validate password
        if not len(postData['password']):
            errors['password'] = "Please enter your password."
        elif not user_list:
            errors['password'] = "This password has not been registered."
        elif not bcrypt.checkpw(postData['password'].encode(),user_list[0].password.encode()):
            errors['password'] = "Wrong password."

        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
