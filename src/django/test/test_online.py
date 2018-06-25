"""
test_online.py.

Test if the server is online.
"""
from django.test import Client
from django.test import TestCase


class IsOnline(TestCase):
    """IsOnline.

    Test is the server is online.
    """

    def setUp(self):
        """Setup."""
        self.c = Client()

    def test_online(self):
        """Test if server is online."""
        response = self.c.get('/admin', follow=True)
        self.assertEquals(response.status_code, 200)
