from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True) # np. USD
    name = models.CharField(max_length=50)           # np. Dolar amerykański
    symbol = models.CharField(max_length=5, blank=True)

    # TA FUNKCJA NAPRAWI WYŚWIETLANIE NA LIŚCIE:
    def __str__(self):
        return f"{self.code} - {self.name}"

class Asset(models.Model):
    user = models.ForeignKey(User, on_python_msg=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    # DLA PORZĄDKU W PANELU ADMINA:
    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency.code}"