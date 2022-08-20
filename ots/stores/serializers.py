from .models import Store
from rest_framework.serializers import ModelSerializer


class StoreSerializer(ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'