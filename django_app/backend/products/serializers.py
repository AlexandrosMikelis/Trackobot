from rest_framework import serializers
from rest_framework.reverse import reverse



from .models import Product
# from . import validators

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'