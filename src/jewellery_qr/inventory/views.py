from django.shortcuts import render, redirect , get_object_or_404
from .forms import ProductForm
from .models import Product

# Add Product View
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            product = form.save()
            return redirect('inventory:product_detail')  # Corrected redirect
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

# Product List View
def product_detail(request):
    products = Product.objects.all()  # Get all products (corrected to use plural 'products')
    print(products)
    return render(request, 'inventory/product_list.html', {'products': products})

# Single Product Detail View
def product_detail_single(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Get the specific product by pk
    return render(request, 'inventory/product_detail.html', {'product': product})

# Home View
def home(request):
    return render(request, 'inventory/home.html', {})

def scan_qr(request):
    return render(request, 'inventory/scan_qr.html', {})

def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_type__icontains=query)  # Case-insensitive search for product type
    else:
        products = Product.objects.all()  # Show all products if no query is provided
    return render(request, 'inventory/product_list.html', {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_detail', product_id=product.product_id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/edit_product.html', {'form': form, 'product': product})