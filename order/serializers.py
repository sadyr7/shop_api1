from rest_framework import serializers
from order.models import Order, OrderItem
class OrderItemSeralizer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = OrderItem
        fields = ('product','product_title', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    products = OrderItemSeralizer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        products = validated_data.pop('products')
        request = self.context.get('request')
        user = request.user
        total_sum = 0

        for product in products:
            try:
                total_sum += product['quantity'] * product['product'].price
            except:
                total_sum += product['product'].price

        order = Order.objects.create(user=user, status='in_process',
                                     total_sum=total_sum, **validated_data)

        for product in products:
            try:
                OrderItem.objects.create(order=order,
                                         product= product['product'],
                                         quantity=product['product'].quantity)
            except:
                OrderItem.objects.create(order=order,
                                         product=product['product'])
        return order

    def to_representation(self, instance, ):
        representation = super().to_representation(instance)
        representation['products'] = OrderItemSeralizer(
            instance.items.all(), many=True
        ).data
        return representation



