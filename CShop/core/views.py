from django.shortcuts import render

from store.models import Product

def frontpage(request):
    """List out newests products on the front pages.
    
    Parameter: request

    Return: Frontpage

    """

    products = Product.objects.filter(status=Product.ACTIVE)
    
    return render(request, 'core/frontpage.html', {
        'products': products
    })

def about(request):
    """Simple about Page.
    
    Parameter: request

    Return: About page

    """

    return render(request, 'core/about.html')