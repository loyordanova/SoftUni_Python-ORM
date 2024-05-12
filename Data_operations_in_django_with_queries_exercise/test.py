from django.test import TestCase

from caller import get_deluxe_rooms
from main_app.models import HotelRoom


class HotelRoomTestCase(TestCase):
    def setUp(self):
        self.room4 = HotelRoom.objects.create(
            room_number=401,
            room_type='Standard',
            capacity=2,
            amenities='TV',
            price_per_night=100.00,
            is_reserved=True
        )

        self.room5 = HotelRoom.objects.create(
            room_number=501,
            room_type='Deluxe',
            capacity=3,
            amenities='Wi-Fi',
            price_per_night=200.00,
            is_reserved=True
        )

        self.room6 = HotelRoom.objects.create(
            room_number=601,
            room_type='Deluxe',
            capacity=6,
            amenities='Jacuzzi',
            price_per_night=400.00,
            is_reserved=False
        )

    def test_zero_get_deluxe_rooms(self):
        """
        Test the get_deluxe_rooms() function when there's only one Deluxe room.
        Ensure it returns the correct information about the deluxe room.

        NOTE: Uses only self.room4; self.room5 and self.room6!!!
        """
        deluxe_rooms = get_deluxe_rooms()
        expected_result = (
            'Deluxe room with number 501 costs 200.00$ per night!'
        )
        self.assertEqual(expected_result, deluxe_rooms)