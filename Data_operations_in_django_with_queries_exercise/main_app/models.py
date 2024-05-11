from django.db import models

# first_exercise --------------------------------------------------------------------------------

class Pet(models.Model):
    name = models.CharField(
        max_length=40
    )

    species = models.CharField(
        max_length=40
    )

# second_exercise --------------------------------------------------------------------------------

class Artifact(models.Model):
    name = models.CharField(
        max_length=70
    )

    origin = models.CharField(
        max_length=70
    )

    age = models.PositiveIntegerField()

    description = models.TextField()

    is_magical = models.BooleanField(
        default=False
    )

# third_exercise --------------------------------------------------------------------------------

class Location(models.Model):
    name = models.CharField(
        max_length=100
    )

    region = models.CharField(
        max_length=50
    )

    population = models.PositiveIntegerField()

    description = models.TextField()

    is_capital = models.BooleanField(
        default=False
    )
