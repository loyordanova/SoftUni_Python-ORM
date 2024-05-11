import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# first_exercise -----------------------------------------------------------------------------------------
from main_app.models import Pet

def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species
    )

    return f"{name} is a very cute {species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# second_exercise -----------------------------------------------------------------------------------------

from main_app.models import Artifact

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifacts = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f'The artifact {name} is {age} years old!'


def delete_all_artifacts():
    Artifact.objects.all().delete()


def rename_artifact(artifact_object, rename_artifact):
    artifact_object.name = rename_artifact
    artifact_object.save()

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))

# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune', True))

# third_exercise -----------------------------------------------------------------------------------------

from main_app.models import Location

def show_all_locations():
    locations = Location.objects.all().order_by('-id')

    result = []

    for location in locations:
        result.append(f'{location.name} has a population of {location.population}!')
    
    return '\n'.join(result)



def new_capital():
    data = Location.objects.first()
    if data:
        data.is_capital = True
        data.save()

    # another way to solve that is faster

    # Location.objects.filter(pk=1).update(is_capital=True)


def get_capitals():
    capitals = Location.objects.filter(is_capital=True).values('name')
    return capitals

def delete_first_location():
    Location.objects.first().delete()

def create():
    Location.objects.create(
            name='Sofia',
            region='Sofia Region',
            population=1329000,
            description='The capital of Bulgaria and the largest city in the country',
            is_capital=False
        )

    Location.objects.create(
            name='Plovdiv',
            region='Plovdiv Region',
            population=346942,
            description='The second-largest city in Bulgaria with a rich historical heritage',
            is_capital=False
        )

    Location.objects.create(
            name='Varna',
            region='Varna Region',
            population=330486,
            description='A city known for its sea breeze and beautiful beaches on the Black Sea',
            is_capital=False
        )
create()
print(show_all_locations())
print(new_capital())
print(get_capitals())
