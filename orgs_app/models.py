from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) < 2:
            errors ['first_name'] = "Name is too short"
        if len(reqPOST['last_name']) < 2:
            errors ['last_name'] = "Name is too short"
        if len(reqPOST['email']) < 6:
            errors ['email'] = "Email too short"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password too short"
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['match'] = "Passwords do not match!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email in wrong format"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email)>= 1:
            errors['dup'] = "Email taken, please create another!"
        return errors

    def login_validator(self, reqPOST):
        errors = {}
        check = User.objects.filter(email=reqPOST['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email in wrong format"
        return errors


class OrgManager(models.Manager):
    def org_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['name']) < 5:
            errors ['name'] = "Name should be at least 5 characters"
        if len(reqPOST['desc']) < 10:
            errors ['desc'] = "Description should be at least 10 characters"
        return errors

class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Org(models.Model):
    name = models.TextField()
    desc = models.TextField()
    added_by = models.ForeignKey(User, related_name='user_who_added', on_delete=models.CASCADE)
    user_who_joined = models.ManyToManyField(User, related_name="user_in_org")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrgManager()