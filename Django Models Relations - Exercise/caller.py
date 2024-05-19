import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book


def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by("id")
    result = []

    for author in authors:
        author_books = Book.objects.filter(author=author).values_list("title", flat=True)
        if author_books:
            result.append(f"{author.name} has written - {', '.join(author_books)}!")

    return "\n".join(result)

def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()