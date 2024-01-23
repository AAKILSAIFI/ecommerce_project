# ecommerce_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .recommender import ProductRecommender
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile

@login_required
def product_list(request):
    recommender = ProductRecommender()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        if product_id and action:
            product = get_object_or_404(Product, id=product_id)

            if action == 'like':
                user_profile.liked_products.add(product)
            elif action == 'dislike':
                user_profile.disliked_products.add(product)

            # You may want to retrain your recommender here based on user actions

    liked_products = user_profile.liked_products.all()
    disliked_products = user_profile.disliked_products.all()
    recommendations = recommender.recommend(request.user.id, liked_products, disliked_products)
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products, 'recommendations': recommendations})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('product_list')

@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Create an order and order items
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Clear the cart
        cart.cartitem_set.all().delete()

        return render(request, 'order_confirmation.html', {'order': order})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
