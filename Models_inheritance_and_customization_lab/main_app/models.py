from datetime import date
from django.db import models
from django.forms import ValidationError

# Create your models here.

class BoolenaChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, 'Available'),
            (False, 'Not Available')
        )

        kwargs['default'] = True

        super().__init__(*args, **kwargs)

# 01. Zoo Animals ---------------------------------------------------------
# 06. Animal's Age --------------------------------------------------------

class Animal(models.Model):
    name = models.CharField(
        max_length=100
    )

    species = models.CharField(
        max_length=100
    )

    birth_date = models.DateField()

    sound = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name
    
    @property
    def age(self):
        current_date = date.today()
        return current_date.year - self.birth_date.year - ((current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day))

    

class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50
    )


class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )


class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50
    )


# 02. Zoo Employees --------------------------------------------------------
# 04. Zookeeper's Specialty ------------------------------------------------

class Employee(models.Model):
    first_name = models.CharField(
        max_length=50
    )

    last_name = models.CharField(
        max_length=50
    )

    phone_number = models.CharField(
        max_length=10
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ZooKeeper(Employee):
    class Specialties(models.TextChoices):
        Mammals = 'Mammals'
        Birds = 'Birds'
        Reptiles = 'Reptiles'
        Others = 'Others'
             
    specialty = models.CharField(
        max_length=10,
        choices=Specialties.choices
    )

    managed_animals = models.ManyToManyField(
        to=Animal
    )

    def clean(self):
        super().clean()

        if self.specialty not in self.Specialties:
            raise ValidationError('Specialty must be a valid choice.')


class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10
    )

    availability = BoolenaChoiceField()

    def is_available(self):
        return self.availability
    

# 03. Animal Display System ----------------------------------------------------
# 05. Animal Display System Logic ----------------------------------------------

class ZooDisplayAnimal(Animal):

    class Meta:
        proxy = True


    def display_info(self):
         return (
            f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. "
            f"It makes a noise like '{self.sound}'."
        )

    
    def is_endangered(self):
        endangered_species = [
            'Cross River Gorilla', 'Orangutan', 'Green Turtle'
        ]
         
        if self.species in endangered_species:
            return f"{self.species} is at risk!"
        else:
            return f"{self.species} is not at risk."