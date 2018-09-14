from decimal import Decimal
from django.conf import settings
from shop.models import Product
# from coupons.models import Coupon


# settings.CART_SESSION_ID = 'cart_id'
# cart = {
#     1: {
#         'quantity': 2,
#         'price': '5200',
#         'product': {'name': '진미채', 'available': True},
#         'total_price': 10400,
#     },
#     2: {
#         'quantity': 1,
#         'price': '6900',
#         'product': {'name': '불고기', 'available': True},
#         'total_price': 6900,
#     },
# }
class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        '''
        sum = 0
        for item in self.cart.values():
            sum = sum + item['quantity']
        return sum
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        # self.session['coupon_id'] = None
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())
