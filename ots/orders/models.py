from django.db import models
from users.models import Profile
from stores.models import Store


class Orders(models.Model):
    CONFIRMED, PACKED, TRANSIT, DELIVERED, CANCELLED = 'confirmed', 'packed', 'transit', 'delivered', 'cancelled'
    status_choice = ((CONFIRMED, 'Confirmed'),
                     (PACKED, 'Packed'),
                     (TRANSIT, 'Transit'),
                     (DELIVERED, 'Delivered'),
                     (CANCELLED, 'Cancelled'))
    COD, PREPAID = 'cod', 'prepaid'
    payment_mode_choice = ((COD, 'cod'), (PREPAID, 'prepaid'))
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(choices=status_choice, max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=24, decimal_places=2)
    payment_mode = models.CharField(choices=payment_mode_choice, max_length=10)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class OrderItem(models.Model):
    CONFIRMED, PACKED, TRANSIT, DELIVERED, CANCELLED = 'confirmed', 'packed', 'transit', 'delivered', 'cancelled'
    status_choice = ((CONFIRMED, 'Confirmed'),
                     (PACKED, 'Packed'),
                     (TRANSIT, 'Transit'),
                     (DELIVERED, 'Delivered'),
                     (CANCELLED, 'Cancelled'))
    sku = models.CharField(max_length=100)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=24, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=status_choice, max_length=12)



# Create your models here.
