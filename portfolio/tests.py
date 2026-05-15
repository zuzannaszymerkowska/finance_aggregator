from django.test import TestCase
from portfolio.models import Currency, Asset
from django.contrib.auth.models import User
from decimal import Decimal

class PortfolioTest(TestCase):
    def setUp(self):
        # Tworzymy użytkownika
        self.user = User.objects.create_user(username='testuser', password='password')
        # TWORZYMY WALUTĘ - to jest kluczowe!
        self.usd = Currency.objects.create(code='USD', name='Dolar', table='A')

    def test_add_asset(self):
        asset = Asset.objects.create(user=self.user, currency=self.usd, amount=Decimal('100.00'))
        self.assertEqual(asset.amount, Decimal('100.00'))