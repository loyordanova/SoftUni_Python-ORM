from datetime import date, timedelta
import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Artist, Car, Owner, Registration, Song, Product, Review, DrivingLicense, Driver


# 01. Library -----------------------------------------------------------

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


# 02. Music App -----------------------------------------------------------
    
def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.all().order_by("-id")


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


# 03. Shop -----------------------------------------------------------
    
def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    total_rating = sum(r.rating for r in reviews)
    avg_rating = total_rating / len(reviews)

    return avg_rating

    # better solution

    # product = Product.objects.annotate(
    #     total_ratings=Sum('review__rating'),
    #     num_reviews = Count('review')
    # ).get(name=product_name)

    # avg_ratings = product.total_ratings / product.num_reviews

    # return avg_ratings


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()

# 04. License -----------------------------------------------------------

# def calculate_licenses_expiration_dates():
#     licenses = DrivingLicense.objects.order_by('-license_number')

#     return '\n'.join(str(l) for l in licenses)

# def get_drivers_with_expired_licenses(due_date: date):
#     exp_cutoff_date = due_date - timedelta(days=365)

#     exp_drivers = Driver.objects.filter(drivinglicense__issue_date__gt=exp_cutoff_date)

#     return exp_drivers
    
def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all()

    final_result = []
    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)

        final_result.append(f"License with number: {license.license_number} expires on {expiration_date}!")

    return '\n'.join(sorted(final_result, reverse=True))


def get_drivers_with_expired_licenses(due_date):
    licenses = DrivingLicense.objects.all()

    final_result_drivers = []
    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)

        if expiration_date > due_date:
            final_result_drivers.append(license.driver)

    return final_result_drivers


# 04. Car Registration -----------------------------------------------------------

def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True, owner=owner).first()

    car.owner = owner

    car.save()

    registration.registration_date = date.today()
    registration.car = car

    registration.save()
 
    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."
