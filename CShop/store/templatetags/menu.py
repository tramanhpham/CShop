from django import template

from store.models import Category

register = template.Library()

@register.inclusion_tag('core/menu.html')
def menu():
    """
    Retrieve the list of categories for the menu.

    Returns:
        dict: A dictionary containing the list of categories.

    """
    categories = Category.objects.all()

    return {'categories': categories}