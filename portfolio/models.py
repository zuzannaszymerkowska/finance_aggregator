from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # np. USD, EUR, CHF
    name = models.CharField(max_length=50)
    table = models.CharField(max_length=1, default='A') # Tabela NBP (A lub B)

    def __clstr__(self):
        return f"{self.name} ({self.code})"

class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=4) # Ilość posiadanej waluty
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.currency.code} - {self.user.username}"

class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('currency', 'date') # Jeden kurs na jeden dzień dla danej waluty