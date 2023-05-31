from django import forms

from .models import Product, Order

class OrderForm(forms.ModelForm):
    """Form for create Order.

    Parameter: forms.ModelForm

    Fields: first name, last name, address city

    """

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'city',)

class ProductForm(forms.ModelForm):
    """Form for create Product.

    Parameter: forms.ModelForm

    Fields: category, title, description, price, image
    
    """

    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
        }