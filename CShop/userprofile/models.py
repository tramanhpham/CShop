from django.contrib.auth.models import User
from django.db import models

class Userprofile(models.Model):
    """
    Model representing a user profile.

    Each user profile is associated with a User model instance using a One-to-One relationship.
    The user profile contains additional information about the user,
    such as whether they are a vendor or not.

    Attributes:
        user (User): The associated User model instance.
        is_vendor (bool): Indicates whether the user is a vendor or not.

    Methods:
        __str__: Returns a string representation of the user profile.

    """
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)
    
    def __str__(self):
        """
        Returns a string representation of the user profile.

        Returns:
            str: The username of the associated user.

        """
        return self.user.username