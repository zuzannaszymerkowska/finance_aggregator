from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Currency, Asset
from .services import NBPService

class PortfolioTests(TestCase):
    def setUp(self):
        # Tworzymy dane testowe
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.usd = Currency.objects.create(code='USD', name='Dolar', table='A')
        self.asset = Asset.objects.create(user=self.user, currency=self.usd, amount=Decimal('100.00'))

    def test_asset_creation(self):
        """Sprawdza czy asset poprawnie zapisuje się w bazie"""
        self.assertEqual(self.asset.amount, Decimal('100.00'))
        self.assertEqual(self.asset.currency.code, 'USD')

    def test_nbp_service_integration(self):
        """Testuje pobieranie kursu (wymaga połączenia z internetem lub zamockowania)"""
        rate_obj = NBPService.get_current_rate('USD')
        self.assertIsNotNone(rate_obj)
        self.assertGreater(rate_obj.rate, 0)