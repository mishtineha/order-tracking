from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Orders, OrderItem
from stores.models import Store
from stores.serializers import StoreSerializer
from django.core.exceptions import ObjectDoesNotExist


class ItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        exclude = ('order',)

    def validate_status(self, value):
        if value not in [OrderItem.CONFIRMED, OrderItem.CANCELLED, OrderItem.PACKED, OrderItem.TRANSIT]:
            raise ValidationError(f"status value should be in {OrderItem.CONFIRMED, OrderItem.CANCELLED, OrderItem.PACKED, OrderItem.TRANSIT}")
        return value

    def create(self, validated_data):
        item = OrderItem(**validated_data)
        item.save()
        return item


class OrderSerializer(ModelSerializer):

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        if kwargs.get('data'):
            self.items = kwargs.get('data').get('items')
            self.store_id = kwargs.get('data').get('store')
    items = ItemSerializer(source='order_items', many=True, read_only=True)

    store_detail = StoreSerializer(source='store', read_only=True)

    def validate(self, data):
        errors = {'items':[]}
        for item in self.items:
            item['status'] = OrderItem.CONFIRMED
            serializer = ItemSerializer(data=item)
            if not serializer.is_valid():
                errors['items'].append(serializer.errors)
        if len(errors['items']) > 0:
            raise ValidationError(errors)
        return data

    def validate_store(self, data):
        try:
            Store.objects.get(id=self.store_id)
        except ObjectDoesNotExist:
            raise ValidationError("incorrect store id")
        return data

    def validate_status(self, value):
        if value not in [Orders.CONFIRMED, Orders.CANCELLED, Orders.PACKED, Orders.TRANSIT]:
            raise ValidationError(
                f"status value should be in {Orders.CONFIRMED, Orders.CANCELLED, Orders.PACKED, Orders.TRANSIT}")
        return value

    def save(self):
        order = Orders(**self.validated_data)
        order.save()
        for item in self.items:
            # item['store'] = Store.objects.get(id=item['store']).id
            serializer = ItemSerializer(data=item)
            """
            this serializer will always be valid as we check its validation in validate method already
            """
            if serializer.is_valid():
                serializer.save(order=order)
        return order

    class Meta:
        model = Orders
        exclude = ('id',)
