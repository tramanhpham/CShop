from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Order, OrderItem, Review

def add_to_cart(request, product_id):
    """
    Adds a product to the cart.

    Retrieves the cart from the session, adds the specified product to the cart,
    and saves the updated cart back to the session. Then, redirects to the cart view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: A redirect response to the cart view.
    """
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')

def remove_from_cart(request, product_id):
    """
    Removes a product from the cart.

    Retrieves the cart from the session, removes the specified product from the cart,
    and saves the updated cart back to the session. Then, redirects to the cart view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: A redirect response to the cart view.
    """
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def change_quantity(request, product_id):
    """
    Changes the quantity of a product in the cart.

    Retrieves the desired action from the request's GET parameters, which can be 'increase' or 'decrease'.
    Based on the action, the quantity is adjusted accordingly for the specified product in the cart.
    The updated cart is saved to the session, and the user is redirected to the cart view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: A redirect response to the cart view.
    """
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

        return redirect('cart_view')

def cart_view(request):
    """
    Renders the cart view.

    Retrieves the cart from the session and passes it to the template for rendering.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response containing the rendered cart view template.
    """
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'cart': cart
    })

@login_required
def checkout(request):
    """
    Handles the checkout process for authenticated users.

    Retrieves the cart from the session and the order form from the request's POST data.
    If the form is valid, calculates the total price of the items in the cart,
    creates an order instance, associates it with the authenticated user,
    sets the paid amount to the total price, and saves the order.
    Additionally, creates order items for each item in the cart.
    Finally, clears the cart and redirects to the 'myaccount' page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: A redirect response to the 'myaccount' page.

    Requires:
        - User to be authenticated.

    """
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return redirect('myaccount')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
    })

def search(request):
    """
    Handles the search functionality.

    Retrieves the search query from the request's GET parameters.
    Filters the active products based on the search query,
    matching either the title or description using case-insensitive search.
    Renders the search results page with the search query and matching products.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response containing the rendered search results page.

    """
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html', {
        'query': query,
        'products': products,
    })

def category_detail(request, slug):
    """
    Renders the detail page for a specific category.

    Retrieves the category object with the specified slug from the database,
    or raises a 404 error if the category does not exist.
    Filters the products belonging to the category based on their active status.
    Renders the category detail page, passing the category and its associated products.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the category.

    Returns:
        HttpResponse: The response containing the rendered category detail page.

    Raises:
        Http404: If the category with the specified slug does not exist.

    """
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)

    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    """
    Renders the detail page for a specific product.

    Retrieves the product object with the specified category slug and product slug from the database,
    filtering by the product's active status.
    If the product does not exist or is not active, raises a 404 error.
    Renders the product detail page, passing the product object.

    Args:
        request (HttpRequest): The request object.
        category_slug (str): The slug of the category the product belongs to.
        slug (str): The slug of the product.

    Returns:
        HttpResponse: The response containing the rendered product detail page.

    Raises:
        Http404: If the product with the specified category slug and product slug does not exist,
                 or if the product is not active.

    """
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)

    if request.method == 'POST':
        rating = request.POST.get('rating', 5)
        content = request.POST.get('content', '')

        if content:
            reviews = Review.objects.filter(created_by=request.user, product=product)

            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    content=content,
                    created_by=request.user
                )

    return render(request, 'store/product_detail.html', {
        'product': product
    })