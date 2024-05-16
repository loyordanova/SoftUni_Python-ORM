import os
from typing import List
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon
from django.db.models import Q, Case, When, Value

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
    # Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    # Laptop.objects.filter(brand='Apple').update(operation_system='MacOS')
    # Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(operation_system='Linux')
    # Laptop.objects.filter(brand='Lenovo').update(operation_system='Chrome OS')


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# 03. Chess Player  -------------------------------------------------------
def bulk_create_chess_players(*args):
    ChessPlayer.objects.bulk_create(*args)

def delete_chess_players():
    ChessPlayer.objects.filter(title="no title").delete()

def change_chess_games_won():
    ChessPlayer.objects.filter(title="GM").update(games_won=30)

def change_chess_games_lost():
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)

def change_chess_games_drawn():
    ChessPlayer.objects.all().update(games_drawn=10)

def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")

def grand_chess_title_IM():
    ChessPlayer.objects.filter(Q(rating__gte=2300) & Q(rating__lt=2400)).update(title="IM")

def grand_chess_title_FM():
    ChessPlayer.objects.filter(Q(rating__gte=2200) & Q(rating__lt=2300)).update(title="FM")

def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__lt=2200).update(title="regular player")

# 03. Meal -------------------------------------------------------

def set_new_chefs():
    Meal.objects.update(
        chef=Case(
            When (meal_type='Breakfast', then=Value('Gordon Ramsay')),
            When (meal_type='Lunch', then=Value('Julia Child')),
            When (meal_type='Dinner', then=Value('Jamie Oliver')),
            When (meal_type='Snack', then=Value('Thomas Keller')),
        )
    )

def set_new_preparation_times():
    Meal.objects.update(
        preparation_time=Case(
            When (meal_type='Breakfast', then=Value('10 minutes')),
            When (meal_type='Lunch', then=Value('12 minutes')),
            When (meal_type='Dinner', then=Value('15 minutes')),
            When (meal_type='Snack', then=Value('5 minutes')),
        )
    )

def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)
    
def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


# 05. Dungeon --------------------------------------------------------------
def bulk_create_dungeons(*args):
    Dungeon.objects.bulk_create(*args)

def show_hard_dungeons():
    # dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')
    # dungeon_info = [
    #     f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!"
    #     for dungeon in dungeons
    # ]
    # return '\n'.join(dungeon_info)

    dungeons = Dungeon.objects.filter(difficulty="Hard").order_by("-location")
    result = []
    for d in dungeons:
        result.append(f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!")
    return "\n".join(result)

def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value('The Erased Thombs')),
            When(difficulty='Medium', then=Value('The Coral Labyrinth')),
            When(difficulty='Hard', then=Value('The Lost Haunt'))
        )
    )

def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)

def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty='Easy', then=Value(25)),
            When(difficulty='Medium', then=Value(50)),
            When(difficulty='Hard', then=Value(75))
        )
    )

def update_dungeon_rewards():
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then =Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet'))
        )
    )

def set_new_locations():
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )