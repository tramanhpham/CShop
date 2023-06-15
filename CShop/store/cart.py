from django.conf import settings

from .models import Product

class Cart(object):
    """
    Represents a shopping cart.

    Attributes:
        session (Session): The session object for the current request.
        cart (dict): The dictionary representing the cart.

    Methods:
        __init__(self, request): Initializes the Cart object.
        __iter__(self): Returns an iterator over the items in the cart.
        __len__(self): Returns the total number of items in the cart.
        save(self): Saves the cart to the session.
        add(self, product_id, quantity=1, update_quantity=False): Adds a product to the cart.
        remove(self, product_id): Removes a product from the cart.
        clear(self): Clears the cart.
        get_total_cost(self): Returns the total cost of all items in the cart.

    """
    def __init__(self, request):
        """
        Initializes the Cart object.

        Parameters:
            request (HttpRequest): The HttpRequest object representing the user's request.

        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """
        Returns an iterator over the items in the cart.

        Yields:
            dict: A dictionary representing an item in the cart.

        """
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity']) / 100

            yield item

    def __len__(self):
        """
        Returns the total number of items in the cart.

        Returns:
            int: The total number of items in the cart.

        """
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """
        Saves the cart to the session.

        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False):
        """
        Adds a product to the cart.

        Parameters:
            product_id (int): The ID of the product to add.
            quantity (int, optional): The quantity of the product to add (default is 1).
            update_quantity (bool, optional): Whether to update the quantity if the product is already in the cart
                                              (default is False).

        """
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)

        self.save()

    def remove(self, product_id):
        """
        Removes a product from the cart.

        Parameters:
            product_id (int): The ID of the product to remove.

        """
        if product_id in self.cart:
            del self.cart[product_id]

            self.save()

    def clear(self):
        """
        Clears the cart.

        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        """
        Returns the total cost of all items in the cart.

        Returns:
            int: The total cost of all items in the cart.

        """
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values())) / 100