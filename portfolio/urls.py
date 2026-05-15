from django.urls import path
from . import views  

urlpatterns = [
    path('', views.portfolio_list, name='portfolio_list'),
    path('add/', views.add_asset, name='add_asset'),
    path('delete/<int:pk>/', views.delete_asset, name='delete_asset'),
]