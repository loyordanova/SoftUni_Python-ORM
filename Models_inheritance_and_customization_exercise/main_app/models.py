from datetime import timedelta
from typing import Any
from django.db import models
from django.forms import ValidationError

# 01. Character Classes -------------------------------------------------------------


class BaseCharacter(models.Model):
    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(
        max_length=100
    )

    spellbook_type = models.CharField(
        max_length=100
    )


class Assassin(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100
    )

    assassination_technique = models.CharField(
        max_length=100
    )


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100
    )

    demon_slaying_ability = models.CharField(
        max_length=100
    )


class TimeMage(Mage):
    time_magic_mastery  = models.CharField(
        max_length=100
    )

    temporal_shift_ability = models.CharField(
        max_length=100
    )


class Necromancer(Mage):
    raise_dead_ability = models.CharField(
        max_length=100
    )


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(
        max_length=100
    )

    venomous_bite_ability = models.CharField(
        max_length=100
    )


class ShadowbladeAssassin(Assassin):
    shadowstep_ability  = models.CharField(
        max_length=100
    )


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(
        max_length=100
    )

    retribution_ability = models.CharField(
        max_length=100
    )


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(
        max_length=100
    )


# 02. Chat App -------------------------------------------------------------------
    
class UserProfile(models.Model):
    username = models.CharField(
        max_length=70,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    bio = models.TextField(
        null=True,
        blank=True
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        to=UserProfile,
        related_name='received_messages',
        on_delete=models.CASCADE
    )

    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def mark_as_read(self) -> None:
        self.is_read = True 
        self.save()

    def reply_to_message(self, reply_content: str):
        reply_message = Message.objects.create(
            sender = self.receiver,  # The receiver of the original message becomes the sender of the reply
            receiver = self.sender,  # The sender of the original message becomes the receiver of the reply
            content = reply_content
        )
        reply_message.save()

        return reply_message
    
    def forward_message(self, receiver: UserProfile):
        forward_message = Message.objects.create(
            sender = self.sender,  # The sender remains the same
            receiver = receiver,   # The new receiver
            content = self.content # The same content is forwarded
        )
        forward_message.save()

        return forward_message
    
# 03. Student Information ----------------------------------------------------------
# CHECK DURING LIVE EXERCISE !!!!
    
class StudentIDField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is None:
            return value

        try:
            # Convert the value to an integer
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError("Invalid input for student ID")

        # Check if the value is positive
        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return value

    def validate(self, value, model_instance):
        # Convert the value to an integer
        value = self.get_prep_value(value)
        super().validate(value, model_instance)

class Student(models.Model):
    name = models.CharField(
        max_length=100
    )

    student_id = StudentIDField()

# 04. Credit Card Masking ---------------------------------------------------------
    
class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20

        super().__init__(*args, **kwargs)
 
    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")
        
        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")
    
        return f"****-****-****-{value[-4:]}"
    

class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100
    )

    card_number = MaskedCreditCardField()

# 05. Hotel Reservation System ------------------------------------------------------
    
class Hotel(models.Model):
    name = models.CharField(
        max_length=100
    )

    address = models.CharField(
        max_length=200
    )

class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE 
    )

    number = models.CharField(
        max_length=100,
        unique=True
    )

    capacity = models.PositiveIntegerField()

    total_guests = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError('Total guests are more than the capacity of the room')

    def save(self, *args, **kwargs) -> str:
        self.clean()
        super().save(*args, **kwargs)

        return f'Room {self.number} created successfully'
    

class BaseReservation(models.Model):

    class Meta:
        abstract = True

    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()

    end_date = models.DateField()


    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days
    

    def calculate_total_cost(self):
        total_cost = self.reservation_period() * self.room.price_per_night

        return round(total_cost, 2)
    

    @property
    def is_available(self):
        reservations = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date
        )

        return not reservations.exists()
    

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError( "Start date cannot be after or in the same end date")
        
        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")
    

class RegularReservation(BaseReservation):
    def save(self, *args, **kwargs):
        super().clean()
        super().save(*args, **kwargs)

        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):
    def save(self, *args, **kwargs):
        super().clean()
        super().save(*args, **kwargs)

        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int):
        reservations = SpecialReservation.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date + timedelta(days=days)
        )

        if reservations:
            raise ValidationError("Error during extending reservation")
        
        self.end_date += timedelta(days=days)
        super().save()

        return f"Extended reservation for room {self.room.number} with {days} days"