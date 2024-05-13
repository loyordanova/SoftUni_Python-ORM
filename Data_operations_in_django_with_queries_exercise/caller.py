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
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f'The artifact {artifact.name} is {artifact.age} years old!'


def delete_all_artifacts():
    Artifact.objects.all().delete()

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

def create_cars():
    Car.objects.create(
        model='Mercedes C63 AMG',
        year='2019',
        color='white',
        price='120000.00'
    )

    Car.objects.create(
        model='Audi Q7 S line',
        year='2023',
        color='black',
        price='183900.00'
    )

    Car.objects.create(
        model='Chevrolet Corvette',
        year='2021',
        color='dark gray',
        price='199999.00'
    )
    


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
    # one way to solve

    # decoded_new_task = ""

    # for char in text:
    #     decoded_new_task += chr(ord(char) - 3)

    # for task in Task.objects.filter(title=task_title):
    #     task.description = decoded_new_task
    #     task.save()
    
    # another way to solve
    
    # matching_title = Task.objects.filter(title=task_title)
    # decoded_text = ''.join(chr(ord(char) - 3) for char in text)

    # for task in matching_title:
    #     task.description = decoded_text
    #     task.save()

    # best way to solve !
        
    decoded_text = ''.join(chr(ord(char) - 3) for char in text)
    Task.objects.filter(title=task_title).update(description=decoded_text)

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


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_capacity = 0

    for room in rooms:
        if not room.is_reserved:
            continue
        if previous_capacity:
            room.capacity += previous_capacity
        else:
            room.capacity += room.id
        
        previous_capacity = room.capacity

        room.save()
        # if room.is_reserved:
        #     if room.id == HotelRoom.objects.first().id:
        #         room.capacity += room.id
        #     else:
        #         room.capacity += previous_capacity
        # room.save()

        # previous_capacity = room.capacity

    

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
# create_room()

# test code:

# reserve_first_room()
# print(get_deluxe_rooms())
# print(HotelRoom.objects.get(room_number=601).is_reserved)
# delete_last_room()


# seventh_exercise -----------------------------------------------------------------------------------------
        
from main_app.models import Character
from django.db.models import Q, F

def update_characters():

    # """
    # F expressions (F()):

    # F() expressions allow you to reference model field values within a query, enabling you to perform operations directly in the database without retrieving the data into Python memory.
    # They are useful for updating or filtering based on the values of other fields within the same model.
    # For example, F("field_name") represents the value of the field field_name in the database.

    # Q objects (Q()):

    # Q() objects are used to encapsulate complex query conditions, such as OR conditions, negations, and combinations of conditions.
    # They allow you to build dynamic queries with multiple conditions using logical operators like AND (&), OR (|), and NOT (~).
    # For example, Q(field1=value1) | Q(field2=value2) represents a query where either field1 equals value1 or field2 equals value2.
    # """

    Character.objects.filter(class_name="Mage").update(
        level=F("level")+3, 
        intelligence=F("intelligence")-7
    )

    Character.objects.filter(class_name="Warrior").update(
        hit_points=F("hit_points") / 2,
          dexterity=F("dexterity") + 4
    )

    Character.objects.filter(Q(class_name="Assassin") | Q(class_name="Scout")).update(
        inventory="The inventory is empty"
    )


    # another way

    # Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
    #     inventory='The inventory is empty'
    # )

    # another way to solve 

    # characters = Character.objects.all()

    # for character in characters:
    #     if character.class_name == 'Mage':
    #         character.level += 3
    #         character.intelligence -= 7
        
    #     elif character.class_name == 'Warrior':
    #         character.hit_points //= 2
    #         character.dexterity += 4
        
    #     else:
    #         character.inventory = 'The inventory is empty'
        
    #     character.save()

def fuse_characters(first_character: Character, second_character: Character):
    fusion_name  = first_character.name + ' ' + second_character.name
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_class = 'Fusion'
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5 
    fusion_hit_points = (first_character.hit_points + second_character.hit_points)

    if first_character.class_name in ['Mage', 'Scout']:
        fusion_inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        fusion_inventory = 'Dragon Scale Armor, Excalibur'
    
    Character.objects.create(
        name=fusion_name,
        class_name=fusion_class,
        level=fusion_level,
        strength=fusion_strength,
        dexterity=fusion_dexterity,
        intelligence=fusion_intelligence,
        hit_points=fusion_hit_points,
        inventory=fusion_inventory
    )

    first_character.delete()
    second_character.delete()

def grand_dexterity():
    Character.objects.update(dexterity=30)

def grand_intelligence():
    Character.objects.update(intelligence=40)

def grand_strength():
    Character.objects.update(strength=50)

def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()