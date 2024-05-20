from django.db import models

# 1.	Library -------------------------------------------------------
class Author(models.Model):
    name = models.CharField(
        max_length=40
    )

class Book(models.Model):
    title = models.CharField(
        max_length=40
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE
    )

# 02.Music App -----------------------------------------------------------

class Song(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True
    )

class Artist(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    songs = models.ManyToManyField(
        to=Song,
        related_name='artists'
    )


# 02.Music App -----------------------------------------------------------

class Product(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )


class Review(models.Model):
    description = models.TextField(
        max_length=200
    )

    rating = models.PositiveIntegerField()

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )


# 04. Licence -----------------------------------------------------------
    
class Driver(models.Model):
    first_name = models.CharField(
        max_length=50
    )

    last_name = models.CharField(
        max_length=50
    )

class DrivingLicense(models.Model):
    license_number = models.CharField(
        max_digits=10,
        unique=True
    )

    issue_date = models.DateField()

    driver = models.OneToOneField(
        to=Driver,
        on_delete=models.CASCADE,
        related_name='license'
    )