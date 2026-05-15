from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset
from .forms import AssetForm  # Upewnij się, że masz ten import!
from .services import NBPService
from decimal import Decimal

@login_required
def portfolio_list(request):
    assets = Asset.objects.filter(user=request.user)
    total_value_pln = Decimal('0.00')
    for asset in assets:
        rate_obj = NBPService.get_current_rate(asset.currency.code)
        if rate_obj:
            asset.current_rate = Decimal(str(rate_obj.rate))
            asset.value_pln = asset.amount * asset.current_rate
            total_value_pln += asset.value_pln
    return render(request, 'portfolio/list.html', {'assets': assets, 'total_value_pln': total_value_pln})

# TEJ FUNKCJI PRAWDOPODOBNIE BRAKUJE LUB MA BŁĄD W NAZWIE:
@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            return redirect('portfolio_list')
    else:
        form = AssetForm()
    return render(request, 'portfolio/add_asset.html', {'form': form})

@login_required
def delete_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    if request.method == 'POST':
        asset.delete()
    return redirect('portfolio_list')