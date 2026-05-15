from django.contrib import admin
from .models import Currency, Asset, ExchangeRate

admin.site.register(Currency)
admin.site.register(Asset)
admin.site.register(ExchangeRate)