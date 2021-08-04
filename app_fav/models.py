from django.db import models
import re
import bcrypt
from datetime import date, datetime
from time import strftime

# Create your models here.

# ----------------------------------------------------------
# UserManager class (for errors and validations)----------->
# ----------------------------------------------------------
class UserManager(models.Manager):
# ----------------------------------------------------------
# registration validator----------->
# ----------------------------------------------------------
    def register_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long!"
            
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long!"
        
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Email address invalid! Please enter a valid email address."

        if User.objects.filter(email = postData['email']).exists() and postData['do_what']== "register":
            errors['email'] = "Could not register. The email address you entered already exists."

        if len(postData['password']) < 8:
            errors['password'] = "Invalid password! Password must be at least 8 characters long."

        if postData['password'] != postData['conf_pass']:
            errors['conf_pass'] = "The password and confirm password did not match! Please re-enter the password."

        return errors
    
# ----------------------------------------------------------
# login validator----------->
# ----------------------------------------------------------
    def login_validator(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['login_email'])

        if len(user)<1:
            errors['login_email'] = "Invalid credentials. Please enter valid email!"
        else:
            logged_user = user[0]
            
            if not bcrypt.checkpw(postData['login_pass'].encode(), logged_user.password.encode()):
                errors['login_email'] = "Invalid password. Please enter valid password"
        
        return errors

# ----------------------------------------------------------
# BookManager class (for errors and validations)----------->
# ----------------------------------------------------------
class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        
        if postData['title'] == "":
            errors['title'] = "Please enter a title!"

        if len(postData['desc']) <5:
            errors['desc'] = "The description must be at least 5 characters long!"

        return errors

# ----------------------------------
# User class (users in DB)----------->
# ----------------------------------
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # liked_books = a list of books a given user likes
    # uploaded_books = a list of books uploaded by a given user
    objects = UserManager()

# ----------------------------------
# Book class (books in DB)----------->
# ----------------------------------
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = "uploaded_books", on_delete = models.CASCADE)
    # user who uploaded a given bookcopy
    users_who_like = models.ManyToManyField(User, related_name = 'liked_books')
    # users_who_like = a list of users who like a given book

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()