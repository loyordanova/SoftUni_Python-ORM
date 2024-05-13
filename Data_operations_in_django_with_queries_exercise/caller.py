from decimal import Decimal
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

# def create_locations():
#     Location.objects.create(
#             name='Sofia',
#             region='Sofia Region',
#             population=1329000,
#             description='The capital of Bulgaria and the largest city in the country',
#             is_capital=False
#         )

#     Location.objects.create(
#             name='Plovdiv',
#             region='Plovdiv Region',
#             population=346942,
#             description='The second-largest city in Bulgaria with a rich historical heritage',
#             is_capital=False
#         )

#     Location.objects.create(
#             name='Varna',
#             region='Varna Region',
#             population=330486,
#             description='A city known for its sea breeze and beautiful beaches on the Black Sea',
#             is_capital=False
#         )
    
# create_locations()
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

# forth_exercise -----------------------------------------------------------------------------------------

from main_app.models import Car

def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        discount = sum(int(num) for num in str(car.year))
        discount_percentage = Decimal(discount) / Decimal(100)
        discount_amount = car.price * discount_percentage
        car.price_with_discount = car.price - discount_amount
        car.save()

def get_recent_cars():
    cars = Car.objects.all().filter(year__gt=2020).values('model', 'price_with_discount')
    return cars

def delete_last_car():
    Car.objects.last().delete()

# def create_cars():
#     Car.objects.create(
#         model='Mercedes C63 AMG',
#         year='2019',
#         color='white',
#         price='120000.00'
#     )

#     Car.objects.create(
#         model='Audi Q7 S line',
#         year='2023',
#         color='black',
#         price='183900.00'
#     )

#     Car.objects.create(
#         model='Chevrolet Corvette',
#         year='2021',
#         color='dark gray',
#         price='199999.00'
#     )
    

# create_cars()
# apply_discount()
# print(get_recent_cars())

# fifth_exercise -----------------------------------------------------------------------------------------

from main_app.models import Task

def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    result = []
    for task in unfinished_tasks:
        result.append(f"Task - {task.title} needs to be done until {task.due_date}!")
    return "\n".join(result)


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    decoded_new_task = ""
    for char in text:
        decoded_new_task += chr(ord(char) - 3)

    for task in Task.objects.filter(title=task_title):
        task.description = decoded_new_task
        task.save()

# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title ='Sample Task') .description)

# sixth_exercise -----------------------------------------------------------------------------------------

from main_app.models import HotelRoom

def get_deluxe_rooms():

    all_deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")

    result = []

    for room in all_deluxe_rooms:
        if room.id % 2 == 0:
            result.append(str(room))

    return "\n".join(result)

# test code
print(get_deluxe_rooms())
def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_capacity = 0

    for room in rooms:

        if room.is_reserved:
            if room.id == HotelRoom.objects.first().id:
                room.capacity += room.id
            else:
                room.capacity += previous_capacity
            room.save()

        previous_capacity = room.capacity


# increase_room_capacity()
def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room():
    if HotelRoom.objects.last().is_reserved:
        HotelRoom.objects.last().delete()

# def create_room():
#         HotelRoom.objects.create(
#             room_number=401,
#             room_type='Standard',
#             capacity=2,
#             amenities='TV',
#             price_per_night=100.00,
#             is_reserved=True
#         )

#         HotelRoom.objects.create(
#             room_number=501,
#             room_type='Deluxe',
#             capacity=3,
#             amenities='Wi-Fi',
#             price_per_night=200.00,
#             is_reserved=True
#         )

#         HotelRoom.objects.create(
#             room_number=601,
#             room_type='Deluxe',
#             capacity=6,
#             amenities='Jacuzzi',
#             price_per_night=400.00,
#             is_reserved=False
#         )
# # create_room()

# test code:

# reserve_first_room()
# print(HotelRoom.objects.get(room_number=601).is_reserved)
# delete_last_room()