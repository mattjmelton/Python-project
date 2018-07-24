from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def user_validator(self, postData):
        print("in the user validator in models")
        print(postData)
        errors = []
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email address")
        if postData['confirm_password'] != postData['password']:
            errors.append("Passwords do not match")
        if len(errors) < 1:
            user = User.objects.create(
                first_name = postData['first_name'],
                last_name = postData['last_name'],
                email = postData['email'],
                password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            )
            return user
        else:
            return errors

    def login_validator(self, postData):
        print("in the Login validator")
        print(postData)
        user_list = User.objects.filter(email=postData['email'])
        if len(user_list) > 0:
            if bcrypt.checkpw(postData['password'].encode(), user_list[0].password.encode()):
                return user_list[0].id 
        return ["Invalid email and/or password."]


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    

