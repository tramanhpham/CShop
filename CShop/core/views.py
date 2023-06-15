from django.shortcuts import render

from store.models import Product

def frontpage(request):
    """
    Display the homepage with a list of active products.

    Parameters:
        request (HttpRequest): The HttpRequest object representing the user's request.

    Returns:
        HttpResponse: The HttpResponse object containing the content of the homepage and the list of products.

    """
    products = Product.objects.filter(status=Product.ACTIVE)
    
    return render(request, 'core/frontpage.html', {
        'products': products
    })

def about(request):
    """
    Display the about page.

    Parameters:
        request (HttpRequest): The HttpRequest object representing the user's request.

    Returns:
        HttpResponse: The HttpResponse object containing the content of the about page.

    """
    return render(request, 'core/about.html')