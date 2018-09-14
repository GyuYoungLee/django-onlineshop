from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('cart:cart_detail')


# 이 페이지에서는 'update': True 로 설정됨
def cart_detail(request):
    cart = Cart(request)
    # 이터레이터 호출됨
    #  item = {
    #       'quantity': 2,
    #       'price': '5200',
    #       'product': {'name': '진미채', 'available': True},
    #       'total_price': 10400,
    #       'update_quantity_form' : {'quantity': 2, 'update': True},
    #  }
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart/cart.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
