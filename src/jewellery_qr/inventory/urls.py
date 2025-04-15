from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('product/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/', views.product_detail_single, name='product_detail_single'),
    path('', views.home, name='home'),
    path('qr_scan/', views.scan_qr, name='scan_qr'),
]
