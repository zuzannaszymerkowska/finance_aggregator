import requests
from .models import Currency, ExchangeRate
from datetime import datetime

class NBPService:
    BASE_URL = "https://api.nbp.pl/api/exchangerates/rates"

    @staticmethod
    def get_current_rate(currency_code):
        try:
            # Szukamy waluty w naszej bazie
            currency = Currency.objects.get(code=currency_code.upper())
            
            # Zapytanie do API NBP
            url = f"{NBPService.BASE_URL}/{currency.table}/{currency.code}/?format=json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            rate_value = data['rates'][0]['mid']
            rate_date = data['rates'][0]['effectiveDate']
            
            # Zapisujemy kurs do naszej bazy danych (ExchangeRate)
            rate_obj, created = ExchangeRate.objects.update_or_create(
                currency=currency,
                date=rate_date,
                defaults={'rate': rate_value}
            )
            return rate_obj
        except Exception as e:
            print(f"Błąd podczas pobierania kursu {currency_code}: {e}")
            return None