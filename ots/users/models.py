from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class AddressBook(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# Create your models here.
