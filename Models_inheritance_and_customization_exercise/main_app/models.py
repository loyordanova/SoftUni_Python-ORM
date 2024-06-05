from django.db import models

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