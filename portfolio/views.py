from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decimal import Decimal  # Dodaj ten import
from .models import Asset
from .services import NBPService

@login_required
def portfolio_list(request):  # Zmieniłem 'self' na 'request' - tak jest poprawnie w Django
    assets = Asset.objects.filter(user=request.user)
    total_value_pln = Decimal('0.00')  # Ustawiamy jako Decimal
    
    for asset in assets:
        rate_obj = NBPService.get_current_rate(asset.currency.code)
        if rate_obj:
            # Rzutujemy na Decimal, aby uniknąć błędu TypeError
            asset.current_rate = Decimal(str(rate_obj.rate))
            asset.value_pln = Decimal(str(asset.amount)) * asset.current_rate
            total_value_pln += asset.value_pln
        else:
            asset.current_rate = Decimal('0.00')
            asset.value_pln = Decimal('0.00')

    return render(request, 'portfolio/list.html', {
        'assets': assets,
        'total_value_pln': total_value_pln
    })