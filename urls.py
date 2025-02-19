from django.urls import path
from .views import *

urlpatterns = [
    path('home', home),
    path('books_view',books_view),
    path('readers', readers_tab),
    path('shopping', shopping),
    path('save', save_customer),
    path('readers/add', save_reader),
    path('login', login),
    path('books', books_tab),
    path('books/add', save_book),
    path('myFav',favourites),
    path('books/add_favorite/<int:book_id>/', add_to_favorites, name='add_to_favorites'),
    path('books/remove_favorite/<int:book_id>/', remove_from_favorites, name='remove_from_favorites'),
]
