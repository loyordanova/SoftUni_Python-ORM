import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book

def show_all_authors_with_their_books():
    authors_data = [
    f'{author.name} has written - {Book.objects.filter(author=author).values_list("title", flat=True)}!'
    for author in Book.objects.all().order_by("id")
    ]

    return '\n'.join(authors_data)

def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()