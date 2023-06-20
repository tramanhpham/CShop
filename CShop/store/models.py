from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from django.core.files import File

from io import BytesIO
from PIL import Image

class Category(models.Model):
    """
    Represents a category.

    Attributes:
        title (CharField): The title of the category.
        slug (SlugField): The slug field for the category's URL.

    Meta:
        verbose_name_plural (str): The plural name for the category model.

    Methods:
        __str__(self): Returns a string representation of the category.

    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        """
        Metadata for the Category model.

        Attributes:
            verbose_name_plural (str): The plural name for the category model.

        """
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Returns a string representation of the category.

        Returns:
            str: The title of the category.

        """
        return self.title

class Product(models.Model):
    """
    Represents a product.

    Attributes:
        DRAFT (str): Constant representing the draft status of a product.
        WAITING_APPROVAL (str): Constant representing the waiting approval status of a product.
        ACTIVE (str): Constant representing the active status of a product.
        DELETED (str): Constant representing the deleted status of a product.
        STATUS_CHOICES (tuple): Choices for the status field of a product.
        user (ForeignKey): Foreign key to the User model representing the owner of the product.
        category (ForeignKey): Foreign key to the Category model representing the category of the product.
        title (CharField): The title of the product.
        slug (SlugField): The slug field for the product's URL.
        description (TextField): The description of the product.
        price (IntegerField): The price of the product.
        image (ImageField): The image of the product.
        thumbnail (ImageField): The thumbnail image of the product.
        created_at (DateTimeField): The date and time when the product was created.
        updated_at (DateTimeField): The date and time when the product was last updated.
        status (CharField): The status of the product.

    Meta:
        ordering (tuple): Specifies the default ordering for the products.

    Methods:
        __str__(self): Returns a string representation of the product.
        get_display_price(self): Returns the display price of the product.
        get_thumbnail(self): Returns the URL of the product's thumbnail image.
        make_thumbnail(self, image, size=(300, 300)): Creates a thumbnail image for the product.

    """
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )

    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnail/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        """
        Metadata for the Product model.

        Attributes:
            ordering (tuple): Specifies the default ordering for the products.

        """
        ordering = ('-created_at',)

    def __str__(self):
        """
        Returns a string representation of the product.

        Returns:
            str: The title of the product.

        """
        return self.title

    def get_display_price(self):
        """
        Returns the display price of the product.

        Returns:
            float: The display price of the product.

        """
        return self.price / 100

    def get_thumbnail(self):
        """
        Returns the URL of the product's thumbnail image.

        Returns:
            str: The URL of the product's thumbnail image.

        """
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url

    def make_thumbnail(self, image, size=(300, 300)):
        """
        Creates a thumbnail image for the product.

        Args:
            image (File): The original image file.
            size (tuple): The desired size of the thumbnail image. Defaults to (300, 300).

        Returns:
            File: The thumbnail image file.

        """
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quantity=85)
        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail

    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating
        
        if reviews_total > 0:
            return reviews_total / self.reviews.count()
        
        return 0

class Order(models.Model):
    """
    Represents an order.

    Attributes:
        first_name (CharField): The first name of the order's recipient.
        last_name (CharField): The last name of the order's recipient.
        address (CharField): The address of the order's recipient.
        city (CharField): The city of the order's recipient.
        paid_amount (IntegerField): The amount paid for the order. Can be blank and null.
        is_paid (CharField): Indicates whether the order is paid or not.
        created_by (ForeignKey): Foreign key to the User model representing the user who created the order.
        created_at (DateTimeField): The date and time when the order was created.

    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    """
    Represents an item in an order.

    Attributes:
        order (ForeignKey): Foreign key to the Order model representing the order that this item belongs to.
        product (ForeignKey): Foreign key to the Product model representing the product associated with this item.
        price (IntegerField): The price of the item.
        quantity (IntegerField): The quantity of the item.

    Methods:
        get_display_price(): Returns the display price of the item, which is the price divided by 100.

    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_display_price(self):
        """
        Returns the display price of the item.

        The display price is calculated by dividing the price by 100.

        Returns:
            float: The display price of the item.

        """
        return self.price / 100

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)