from django.test import TestCase
from django.contrib.auth.models import User
from .models import Currency, Asset

class PortfolioTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Usuwamy 'table', bo model go nie posiada (lub nazywa się inaczej)
        self.usd = Currency.objects.create(code='USD', name='Dolar') 

    def test_add_asset(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post('/add/', {
            'currency': self.usd.id,
            'amount': '100.00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Asset.objects.count(), 1)