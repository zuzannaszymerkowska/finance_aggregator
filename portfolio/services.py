import requests
from django.core.cache import cache
from .models import Currency, ExchangeRate

class NBPService:
    BASE_URL = "https://api.nbp.pl/api/exchangerates/rates"

    @staticmethod
    def get_current_rate(currency_code):
        cache_key = f"rate_{currency_code.upper()}"
        cached_rate = cache.get(cache_key)

        if cached_rate:
            print(f"DEBUG: Pobrano kurs {currency_code} z CACHE")
            return cached_rate

        try:
            currency = Currency.objects.get(code=currency_code.upper())
            url = f"{NBPService.BASE_URL}/{currency.table}/{currency.code}/?format=json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            rate_value = data['rates'][0]['mid']
            rate_date = data['rates'][0]['effectiveDate']
            
            rate_obj, _ = ExchangeRate.objects.update_or_create(
                currency=currency,
                date=rate_date,
                defaults={'rate': rate_value}
            )

            # Zapisz w cache na 5 minut (300 sekund)
            cache.set(cache_key, rate_obj, timeout=300)
            print(f"DEBUG: Pobrano kurs {currency_code} z API NBP i zapisano w CACHE")
            return rate_obj
            
        except Exception as e:
            print(f"Błąd: {e}")
            return None