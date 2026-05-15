import requests
from django.core.cache import cache
from .models import Currency
from decimal import Decimal

class NBPService:
    BASE_URL = "https://api.nbp.pl/api/exchangerates/rates"

    @staticmethod
    def get_current_rate(currency_code):
        cache_key = f"rate_{currency_code.upper()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            print(f"DEBUG: Pobrano kurs {currency_code} z CACHE")
            # Zwracamy obiekt z atrybutem .rate, żeby widoki nie wywalały błędu
            class Rate:
                def __init__(self, r): self.rate = r
            return Rate(cached_data)

        try:
            currency = Currency.objects.get(code=currency_code.upper())
            # Używamy pola 'table' z modelu Currency (zazwyczaj 'A')
            table = getattr(currency, 'table', 'A') 
            url = f"{NBPService.BASE_URL}/{table}/{currency.code}/?format=json"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            rate_value = Decimal(str(data['rates'][0]['mid']))
            
            # Zapisujemy w cache tylko samą liczbę (kurs)
            cache.set(cache_key, rate_value, timeout=300)
            print(f"DEBUG: Pobrano kurs {currency_code} z API NBP i zapisano w CACHE")
            
            # Tworzymy tymczasowy obiekt "na niby", żeby widok mógł zrobić .rate
            class Rate:
                def __init__(self, r): self.rate = r
            return Rate(rate_value)
            
        except Exception as e:
            print(f"Błąd NBP Service: {e}")
            return None