from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_products(request):
    products = Product.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'products/manage_products.html', {'products': products})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, id):
    product = get_object_or_404(Product, id=id, created_by=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_product(request, id):
    product = get_object_or_404(Product, id=id, created_by=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('manage_products')
