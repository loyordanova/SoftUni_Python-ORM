from django.test import TestCase

from caller import show_all_locations
from main_app.models import Location


class LocationTestCase(TestCase):
    def setUp(self):
        """
        SetUp only for the zero tests
        """
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

    def test_zero_show_all_locations(self):
        """
        Test whether the show_all_locations function returns all locations sorted by ID (descending).
        """
        response = show_all_locations()
        expected_output = (
            'Varna has a population of 330486!\n'
            'Plovdiv has a population of 346942!\n'
            'Sofia has a population of 1329000!'
        )
        self.assertEqual(response.strip(), expected_output)
