set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

if [ "$CREATE_SUPERUSER" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$DJANGO_SUPERUSER_USERNAME").exists():
    User.objects.create_superuser("$DJANGO_SUPERUSER_USERNAME", "$DJANGO_SUPERUSER_EMAIL", "$DJANGO_SUPERUSER_PASSWORD")
    print("Superuser created.")
else:
    print("Superuser already exists.")
END
fi

python manage.py shell << END
from portfolio.models import Currency
currencies = [
    {'code': 'USD', 'name': 'Dolar amerykanski', 'symbol': '$', 'table': 'A'},
    {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'table': 'A'},
    {'code': 'CHF', 'name': 'Frank szwajcarski', 'symbol': 'CHF', 'table': 'A'},
    {'code': 'GBP', 'name': 'Funt brytyjski', 'symbol': '£', 'table': 'A'},
]
for data in currencies:
    obj, created = Currency.objects.get_or_create(code=data['code'], defaults=data)
    if created:
        print(f"Dodano walute: {data['code']}")
END

echo "Build script finished successfully"