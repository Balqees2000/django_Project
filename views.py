
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .models import reader

# starting with our function
# functions defined here will be called by django when user make actions
def home(request):
    return render(request,"home.html",context={"current_tab": "home"})

def readers(request):
    return render(request,"readers.html",context={"current_tab": "readers"})

def shopping(request):
    return HttpResponse("Welcome to shopping")

def login(request):
    return render(request,"login.html",context={"current_tab": "login"})

def favourites(request):
    return render(request,"favourites.html",context={"current_tab": "favourites"})

def books_view(request):
     return render(request,"books.html",context={"current_tab": "books"})

def save_customer(request):
    customer_name = request.POST['customer_name']
    return render(request,"welcome.html",context={'customer_name':customer_name})

def readers_tab(request):
    if request.method=="GET":
      readers = reader.objects.all()
      return render(request,"readers.html",context={"current_tab":"readers",
      "readers":readers})
    else:
        # This will execute the query coming from the UI 
        query = request.POST['query']
        readers = reader.objects.raw("select * from library_reader where reader_name like '%"+query+"%'")
        return render(request,"readers.html",context={"current_tab":"readers",
      "readers":readers,
      "query":query
      })

def login(request):
    if request.method == "POST":
        reader_name = request.POST['reader_name']
        reader_password = request.POST['reader_password']

        try:
            user = reader.objects.get(reader_name=reader_name)
            if user.reader_password == reader_password:
                request.session['reference_id'] = user.reference_id
                return redirect('/books')
            else:
                messages.error(request, "Incorrect password.")
        except reader.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, "login.html", context={"current_tab": "login"})

def save_reader(request):
    reader_item = reader(reference_id=request.POST['reader_ref_id'],
                         reader_name=request.POST['reader_name'],
                         readers_contact=request.POST['readers_contact'],
                         reader_password=request.POST['reader_password'],
                         reader_address=request.POST['reader_address'],
                         active= True
                         )
    reader_item.save()
    return redirect('/readers')

def save_book(request):
    book_item = books(
    book_id = request.POST['book_id'],
    book_name = request.POST['book_name'],
    book_author = request.POST['book_author'],
    book_type = request.POST['book_type'],
    available= True
)
    book_item.save()
    return redirect('/books')

def books_tab(request):
    reference_id = request.session.get('reference_id')
    user_favorites = []

    if reference_id:
        try:
            reader_instance = reader.objects.get(reference_id=reference_id)
            user_favorites = Favorite.objects.filter(reader=reader_instance).values_list('book__book_id', flat=True)
        except reader.DoesNotExist:
            pass 

    if request.method == "GET":
        book_list = books.objects.all()
    else:
        query = request.POST.get('query', '')
        book_list = books.objects.raw("SELECT * FROM library_books WHERE book_name LIKE '%%" + query + "%%' OR book_author LIKE '%%" + query + "%%'")

    return render(request, "books.html", {
        "current_tab": "books",
        "book_list": book_list,
        "user_favorites": user_favorites,
        "query": request.POST.get('query', '') if request.method == "POST" else ''
    })

def add_to_favorites(request, book_id):
    reference_id = request.session.get('reference_id')

    if reference_id:
        try:
            reader_instance = reader.objects.get(reference_id=reference_id)
            book = books.objects.get(book_id=book_id)

            favorite, created = Favorite.objects.get_or_create(reader=reader_instance, book=book)

            if created:
                messages.success(request, f"'{book.book_name}' has been added to your favorites.")
            else:
                messages.info(request, f"'{book.book_name}' is already in your favorites.")
            
            return redirect('/books') 
        except books.DoesNotExist:
            messages.error(request, "Book not found.")
    else:
        messages.error(request, "You must be logged in to add favorites.")
       
        return redirect('/login')  
   
    return redirect('/books') 


def books_list(request):
    book_list = books.objects.all()
    reference_id = request.session.get('reference_id')

    user_favorites = []
    if reference_id:
        try:
            reader_instance = reader.objects.get(reference_id=reference_id)
            user_favorites = Favorite.objects.filter(reader=reader_instance).values_list('book_id', flat=True)
        except reader.DoesNotExist:
            pass

    return render(request, 'books.html', {'book_list': book_list, 'user_favorites': user_favorites})

def remove_from_favorites(request, book_id):
    reference_id = request.session.get('reference_id')

    if reference_id:
        try:
            reader_instance = reader.objects.get(reference_id=reference_id)
            book = books.objects.get(book_id=book_id)

            favorite = Favorite.objects.filter(reader=reader_instance, book=book)
            if favorite.exists():
                favorite.delete()
                messages.success(request, f"'{book.book_name}' has been removed from your favorites.")
            else:
                messages.info(request, f"'{book.book_name}' is not in your favorites.")
            return redirect('/books') 
        except reader.DoesNotExist:
            messages.error(request, "Reader not found. Please log in again.")
            return redirect('/login')
        except books.DoesNotExist:
            messages.error(request, "Book not found.")
            return redirect('/books')
    else:
        messages.error(request, "You must be logged in to remove favorites.")
        return redirect('/login')

def favourites(request):
    reference_id = request.session.get('reference_id')
    favorite_books = []
    suggested_books = []

    if reference_id:
        try:
            reader_instance = reader.objects.get(reference_id=reference_id)
            favorite_books = Favorite.objects.filter(reader=reader_instance).values_list('book__book_id', 'book__book_name', 'book__book_author', 'book__book_type', 'book__available')

            if favorite_books:
                favorite_book_types = set([book[3] for book in favorite_books]) 
                suggested_books = books.objects.filter(book_type__in=favorite_book_types).exclude(book_id__in=[book[0] for book in favorite_books])
        except reader.DoesNotExist:
            print("Reader not found")
            pass

    return render(request, "favourites.html", {
        "current_tab": "favourites",
        "favorite_books": favorite_books,
        "suggested_books": suggested_books
    })

