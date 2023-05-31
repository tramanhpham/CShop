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
    """Become vendor.

    Parameter: request

    Return: My store

    """ 

    if request.method == 'POST':
        user = request.user
  
        user.userprofile.is_vendor = True
        user.userprofile.save()
     
        return redirect('my_store')
    
    return render(request, 'userprofile/become_vendor.html')

def vendor_detail(request, pk):
    """Vendor detail.

    Parameter: request, pk

    Return: Vendor detail

    """ 

    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products': products
    })

@login_required
def my_store(request):
    """My store, login required.

    Parameter: request

    Return: My store

    """ 
    
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, 'userprofile/my_store.html', {
        'products': products,
        'order_items': order_items
    })

@login_required
def my_store_order_detail(request, pk):
    """My store order detail, login required.

    Parameter: request, pk

    Return: My store order detail

    """ 
    
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_store_order_detail.html', {
        'order': order
    })

@login_required
def add_product(request):
    """Add product, login required.

    Parameter: request

    Return: Add product

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
    """Edit product, login required.

    Parameter: request, pk

    Return: Edit product

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
    """Delete product, login required.

    Parameter: request, pk

    Return: Delete product

    """ 
    
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'The product was deleted!')

    return redirect('mystore')

@login_required
def myaccount(request):
    """My account, login required.

    Parameter: request

    Return: My account

    """ 
    
    return render(request, 'userprofile/myaccount.html')

def signup(request):
    """Sign up.

    Parameter: request

    Return: Signup

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