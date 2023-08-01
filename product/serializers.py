from rest_framework import serializers
from django.db.models import Avg
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.ratings.aggregate(
            Avg('rating')
        )
        rating = representation['rating']
        rating['rating_count'] = instance.ratings.count()
        return representation