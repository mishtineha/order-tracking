from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
# Create your models here.
