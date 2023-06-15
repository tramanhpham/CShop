from django import forms

from .models import Product, Order

class OrderForm(forms.ModelForm):
    """
    A form for creating an order.

    Attributes:
        Meta (class): Inner class that defines the metadata for the form.

    """
    class Meta:
        """
        Metadata for the OrderForm.

        Attributes:
            model (Model): The model class associated with the form.
            fields (list): The list of fields to include in the form.

        """
        model = Order
        fields = ('first_name', 'last_name', 'address', 'city',)

class ProductForm(forms.ModelForm):
    """
    A form for creating or updating a product.

    Attributes:
        Meta (class): Inner class that defines the metadata for the form.

    """
    class Meta:
        """
        Metadata for the ProductForm.

        Attributes:
            model (Model): The model class associated with the form.
            fields (list): The list of fields to include in the form.
            widgets (dict): Custom widgets for the form fields.

        """
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