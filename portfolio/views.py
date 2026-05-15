from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset
from .forms import AssetForm  
from .services import NBPService
from decimal import Decimal, ROUND_HALF_UP

@login_required
def portfolio_list(request):
    assets = Asset.objects.filter(user=request.user)
    total_value_pln = Decimal('0.00')
    
    twoplaces = Decimal('0.01')
    
    for asset in assets:
        rate_obj = NBPService.get_current_rate(asset.currency.code)
        if rate_obj:
            asset.current_rate = Decimal(str(rate_obj.rate)).quantize(twoplaces, rounding=ROUND_HALF_UP)
            
            asset.value_pln = (asset.amount * asset.current_rate).quantize(twoplaces, rounding=ROUND_HALF_UP)
            
            total_value_pln += asset.value_pln
            
    total_value_pln = total_value_pln.quantize(twoplaces, rounding=ROUND_HALF_UP)
    
    return render(request, 'portfolio/list.html', {
        'assets': assets, 
        'total_value_pln': total_value_pln
    })

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