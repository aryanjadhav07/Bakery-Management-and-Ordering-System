from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', '1kg')
        cart = request.session.get('cart', {})
        
        product = get_object_or_404(Product, id=product_id)
        
        # Select price based on size with safety fallback
        price = 0
        if size == 'half':
            price = product.price_half_kg if product.price_half_kg else product.price
        elif size == '1kg':
            price = product.price_1kg if product.price_1kg else product.price
        elif size == '2kg':
            price = product.price_2kg if product.price_2kg else product.price
        else:
            price = product.price
            
        # Composite key to allow different sizes of the same product in the cart
        item_key = f"{product_id}_{size}"
        
        if item_key in cart:
            cart[item_key]['quantity'] += quantity
        else:
            cart[item_key] = {
                'product_id': product_id,
                'quantity': quantity,
                'size': size,
                'price': float(price),
            }
        
        request.session['cart'] = cart
        messages.success(request, f'Added {product.name} ({size}) to cart.')
    return redirect('products')

@login_required
def remove_from_cart(request, item_key):
    cart = request.session.get('cart', {})
    if item_key in cart:
        del cart[item_key]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    grand_total = 0
    
    for item_key, entry in cart.items():
        if isinstance(entry, dict):
            product_id = entry.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            quantity = entry.get('quantity', 1)
            size = entry.get('size')
            price = entry.get('price', float(product.price))
        else:
            product = get_object_or_404(Product, id=item_key)
            quantity = entry
            size = None
            price = float(product.price)
            
        total = price * quantity
        grand_total += total
        items.append({
            'item_key': item_key,
            'product': product,
            'quantity': quantity,
            'size': size,
            'price': price,
            'total': total,
        })
        
    return render(request, 'orders/cart.html', {'items': items, 'grand_total': grand_total})

@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')
        
    selected_baker_id = request.session.get('selected_baker_id')
    if not selected_baker_id:
        return redirect('/users/select-baker/?next=/place-order/')
        
    baker = get_object_or_404(User, id=selected_baker_id)
    
    # Calculate total and create Order
    grand_total = 0
    items_data = []
    
    for item_key, entry in cart.items():
        if isinstance(entry, dict):
            product_id = entry.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            quantity = entry.get('quantity', 1)
            price = entry.get('price', float(product.price))
            size = entry.get('size')
        else:
            product = get_object_or_404(Product, id=item_key)
            quantity = entry
            price = float(product.price)
            size = None
            
        total = price * quantity
        grand_total += total
        items_data.append({'product': product, 'quantity': quantity, 'price': price, 'size': size})
        
    order = Order.objects.create(
        user=request.user,
        baker=baker,
        total_price=grand_total,
        status='Pending'
    )
    
    # Create OrderItems
    for data in items_data:
        OrderItem.objects.create(
            order=order,
            product=data['product'],
            quantity=data['quantity'],
            price=data['price'],
            size=data['size']
        )
        
    # Clear cart
    request.session['cart'] = {}
    
    return redirect('payment', order_id=order.id)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Don't mark completed yet, redirect to upload receipt
        return redirect('upload_receipt', order_id=order.id)
        
    return render(request, 'orders/payment.html', {'order': order})

@login_required
def upload_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        if 'receipt_image' in request.FILES:
            order.receipt_image = request.FILES['receipt_image']
            order.status = 'Paid'
            order.save()
            messages.success(request, 'Receipt uploaded successfully! Awaiting baker confirmation.')
            return redirect('my_orders')
        else:
            messages.error(request, 'Please select an image file.')
    return render(request, 'orders/upload_receipt.html', {'order': order})

@login_required
def manage_orders(request):
    if not request.user.is_staff:
        return redirect('dashboard')
        
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = get_object_or_404(Order, id=order_id)
        
        if action == 'accept':
            order.status = 'Accepted'
        elif action == 'bake':
            order.status = 'Baking'
        elif action == 'complete':
            order.status = 'Completed'
        order.save()
        messages.success(request, f'Order #{order.id} status updated to {order.status}.')
        return redirect('manage_orders')
        
    orders = Order.objects.filter(baker=request.user).order_by('-created_at')
    return render(request, 'orders/manage_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    order = get_object_or_404(Order, id=order_id, baker=request.user)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        order.status = 'Cancelled'
        order.cancel_reason = reason
        order.save()
        messages.success(request, f'Order #{order.id} cancelled successfully.')
    return redirect('manage_orders')
