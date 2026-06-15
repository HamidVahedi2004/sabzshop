from shop.models import *

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            self.session['cart'] = {}
            cart = self.session['cart']
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1}
        elif self.cart[product_id]['quantity'] < product.inventory:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_post_price(self):
        if len(self.cart) == 0:
            return 0
        if self.get_total_price() < 100000:
            return 82000
        return 0

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            item_data = {
                'product': product,
                'quantity': item['quantity'],
                'price': product.new_price,
                'weight': product.weight,
                'total': product.new_price * item['quantity']
            }
            yield item_data

    def get_total_price(self):
        return sum(item['total'] for item in self)

    def get_final_price(self):
        return self.get_total_price() + self.get_post_price()

    def save(self):
        self.session.modified = True