from django.contrib import admin
from .models import Currency, Asset # Usunięto ExchangeRate

admin.site.register(Currency)
admin.site.register(Asset)