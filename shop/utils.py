from shop.models import Cart

def get_cart(request):
    cart_id = request.session.get('cart-id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart-id'] = cart.id
    return cart