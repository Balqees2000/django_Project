# Create your models here.
# Here will be create classes which will be the tables in sqlite


from django.db import models

# when we run the model

# data model for readers table that will be created in the database
class reader(models.Model):
    # to show the reader name in the list view in our model
    def __str__(self):
        return self.reader_name
    # means this field can store up to 200 chars
    reference_id=models.CharField(max_length=200, unique=True)
    reader_name=models.CharField(max_length=200)
    readers_contact=models.CharField(max_length=200)
    reader_address=models.TextField()
    reader_password = models.CharField(max_length=20, unique=True)
    active=models.BooleanField(default=True)


class books(models.Model):
    book_id = models.CharField(max_length=200, unique=True)
    book_name = models.TextField()
    book_author = models.TextField()
    book_type = models.TextField()
    available = models.BooleanField(default=True)

class Favorite(models.Model):
    reader = models.ForeignKey('reader', on_delete=models.CASCADE)
    book = models.ForeignKey('books', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
         # Ensure that the same book cannot be added multiple times for the same user
        unique_together = ('reader', 'book')

    def __str__(self):
        return f"{self.reader.reader_name} - {self.book.book_name}"

