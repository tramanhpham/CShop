from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from .models import Userprofile

from store.forms import ProductForm
from store.models import Product, OrderItem, Order

@login_required
def become_vendor(request):
    """
    Marks the authenticated user as a vendor.

    If the request method is POST, retrieves the authenticated user and updates their user profile
    to set the 'is_vendor' attribute to True. Saves the user profile.
    Redirects to the 'my_store' page upon successful update.
    If the request method is not POST, renders the 'become_vendor' page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response to redirect to the 'my_store' page or render the 'become_vendor' page.

    """
    if request.method == 'POST':
        user = request.user
  
        user.userprofile.is_vendor = True
        user.userprofile.save()
     
        return redirect('my_store')
    
    return render(request, 'userprofile/become_vendor.html')

def vendor_detail(request, pk):
    """
    Renders the vendor detail page for a specific user.

    Retrieves the user with the given primary key (pk) from the User model.
    Filters the products associated with the user, keeping only those with an 'ACTIVE' status.
    Renders the 'vendor_detail' template with the user and products as context variables.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the user.

    Returns:
        HttpResponse: The response containing the rendered 'vendor_detail' template.

    """
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products': products
    })

@login_required
def my_store(request):
    """
    Renders the 'my_store' page for the authenticated user.

    Retrieves the products associated with the authenticated user, excluding those with a 'DELETED' status.
    Retrieves the order items associated with products owned by the authenticated user.
    Renders the 'my_store' template with the products and order items as context variables.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response containing the rendered 'my_store' template.

    Raises:
        PermissionDenied: If the user is not authenticated.

    """    
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, 'userprofile/my_store.html', {
        'products': products,
        'order_items': order_items
    })

@login_required
def my_store_order_detail(request, pk):
    """
    Renders the 'my_store_order_detail' page for the authenticated user.

    Retrieves the order object with the specified primary key (pk).
    If the order does not exist, a 404 page is displayed.
    Renders the 'my_store_order_detail' template with the order as a context variable.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the order.

    Returns:
        HttpResponse: The response containing the rendered 'my_store_order_detail' template.

    Raises:
        PermissionDenied: If the user is not authenticated.

    """    
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_store_order_detail.html', {
        'order': order
    })

@login_required
def add_product(request):
    """
    Renders the 'add_product' page for the authenticated user.

    If the request method is POST, processes the submitted form data.
    Validates the form and saves the product if it is valid.
    Displays a success message and redirects to 'my_store' page.
    
    If the request method is not POST, renders an empty form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response containing the rendered 'product_form' template.

    Raises:
        PermissionDenied: If the user is not authenticated.

    """  
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')

            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()  

            messages.success(request, 'The product was added!')

            return redirect('my_store') 
    else:
        form = ProductForm()

    return render(request, 'userprofile/product_form.html', {
        'title': 'Add product',
        'form': form
    })

@login_required
def edit_product(request, pk):
    """
    Renders the 'edit_product' page for the authenticated user.

    Retrieves the product with the given primary key (pk) that belongs to the authenticated user.
    
    If the request method is POST, processes the submitted form data.
    Validates the form and saves the changes if it is valid.
    Displays a success message and redirects to 'my_store' page.
    
    If the request method is not POST, renders the form filled with the product's existing data.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the product to be edited.

    Returns:
        HttpResponse: The response containing the rendered 'product_form' template.

    Raises:
        PermissionDenied: If the user is not authenticated or the product does not belong to the user.

    """    
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            
            messages.success(request, 'The changes was saved!')

            return redirect('my_store')
    else:
        form = ProductForm(instance=product)

    return render(request, 'userprofile/product_form.html', {
        'title': 'Edit product',
        'product': product,
        'form': form
    })

@login_required
def delete_product(request, pk):
    """
    Deletes a product belonging to the authenticated user.

    Retrieves the product with the given primary key (pk) that belongs to the authenticated user.
    Sets the status of the product to 'deleted' and saves the changes.
    Displays a success message and redirects to the 'mystore' page.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the product to be deleted.

    Returns:
        HttpResponse: The response redirecting to the 'mystore' page.

    Raises:
        PermissionDenied: If the user is not authenticated or the product does not belong to the user.

    """        
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'The product was deleted!')

    return redirect('mystore')

@login_required
def myaccount(request):
    """
    Render the 'myaccount' page for the authenticated user.

    Returns:
        HttpResponse: The rendered 'myaccount' template.
    """
    return render(request, 'userprofile/myaccount.html')

def signup(request):
    """
    Registers a new user and creates a corresponding user profile.

    If the request method is POST, it creates a new user based on the submitted form data.
    If the form is valid, the user is registered, logged in, and a user profile is created.
    Finally, the user is redirected to the 'frontpage' view.

    If the request method is GET, it displays the user registration form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response redirecting to the 'frontpage' view after successful registration.
        HttpResponse: The response rendering the user registration form for GET requests.

    """    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })