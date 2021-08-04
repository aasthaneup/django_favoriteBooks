from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "logreg.html")

def main(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login before continuing")
        return redirect('/')
    else:
        context = {
            'logged_user' : User.objects.get(id = request.session['userid']),
            'all_books' : Book.objects.all()
        }
        return render(request, 'main.html', context)

def register(request):

    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/")

    else:
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashpw
        )
        request.session['userid'] = new_user.id

        return redirect('/books')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/")
    else:
        user = User.objects.filter(email = request.POST['login_email'])
        request.session['userid'] = user[0].id
        return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')

def upload_book(request, id):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

    else:
        this_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = User.objects.get(id = request.session['userid'])
        )
        this_book.users_who_like.add(User.objects.get(id = request.session['userid']))

    return redirect('/books')

def display_book(request, id):

    context = {
        'this_book' : Book.objects.get(id = id),
        'logged_user' : User.objects.get(id = request.session['userid'])
    }

    return render(request, 'info.html', context)

def update_desc(request, id):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

    else:
        book_to_update = Book.objects.get(id = id)
        book_to_update.desc = request.POST['desc']
        book_to_update.save()
    
    return redirect(f'/books/{id}')

def delete_book(request, id):
    Book.objects.get(id = id).delete()
    return redirect('/books')

def add_to_fav(request, id):
    this_book = Book.objects.get(id = id)
    this_book.users_who_like.add(User.objects.get(id = request.session['userid']))

    return redirect(f'/books/{id}')

def remove_from_fav(request, id):
    this_book = Book.objects.get(id = id)
    this_book.users_who_like.remove(User.objects.get(id = request.session['userid']))

    return redirect(f'/books/{id}')

def remove_from_fav_in_profile(request, id):
    this_book = Book.objects.get(id = id)
    logged_user_id = request.session['userid']
    this_book.users_who_like.remove(User.objects.get(id = logged_user_id))

    return redirect(f'/profile/{logged_user_id}')

def user_profile(request, id):
    if 'userid' not in request.session:
        messages.error(request, "Please login before continuing")
        return redirect('/')
    else:
        logged_user = User.objects.get(id = request.session['userid'])
        context = {
            'logged_user' : logged_user,
            'all_fav_books' : logged_user.liked_books.all()
        }
        return render (request, 'profile.html', context)