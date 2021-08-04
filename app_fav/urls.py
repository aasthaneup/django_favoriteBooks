from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.main),
    path('upload/<int:id>', views.upload_book),
    path('books/<int:id>', views.display_book),
    path('update/<int:id>', views.update_desc),
    path('delete/<int:id>', views.delete_book),
    path('add_to_fav/<int:id>', views.add_to_fav),
    path('remove_from_fav/<int:id>', views.remove_from_fav),
    path('profile/<int:id>', views.user_profile),
    path('remove_from_profile/<int:id>', views.remove_from_fav_in_profile),
    path('logout', views.logout),
]