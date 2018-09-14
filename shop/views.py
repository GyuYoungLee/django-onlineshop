from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views.generic.list import ListView
from cart.forms import CartAddProductForm


# categories : 반찬, 브런치
# category   : 반찬
# products   : 진미채, 불고기
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})


# product : 진미채
# cart_product_form - quantity
# cart_product_form - update
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})
