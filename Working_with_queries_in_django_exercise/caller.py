import os
from typing import List
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop
from django.db.models import Q, Case, When, Value, F

# 01. Artwork Gallery -------------------------------------------------------

def show_highest_rated_art():
    highest_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()

artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)

# Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())


# 02. Laptop  -------------------------------------------------------

def show_the_most_expensive_laptop():
    top_laptop = Laptop.objects.order_by("-price", "id").first()

    return f"{top_laptop.brand} is the most expensive laptop available for {top_laptop.price}$!"

def bulk_create_laptops(*args):
    Laptop.objects.bulk_create(*args)

def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=["Asus", "Lenovo"]).update(storage=512)

    # another solution
    # Laptop.objects.filter(Q(brand="Asus") | Q(brand="Lenovo").update(storage=512)

def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=["Apple", "Dell", "Acer"]).update(memory=16)

def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand="Asus", then=Value("Windows")),
            When(brand="Apple", then=Value("MacOS")),
            When(brand__in=["Dell", "Acer"], then=Value("Linux")),
            When(brand="Lenovo", then=Value("Chrome OS"))
        )
    )
    # another solution
    

def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()
