""" Profile Model """

# Django
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Profile Model 
    
    Model that extends the user model and add extra information of the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone_number = models.CharField(
        max_length=20, 
        blank=True
    )

    def __str__(self):
        """Returns string representation of user"""
        return self