from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.permissions import IsAuthor
from product.serializers import ProductSerializer
from rest_framework.decorators import action
from rating.serializers import RatingSerializer
from rest_framework.response import Response


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return (permissions.IsAuthenticated(), IsAuthor())
        return (permissions.IsAuthenticatedOrReadOnly(),)


# localhost:8000/api/products/rating
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def ratings(self, request, pk):
        product = self.get_object()
        user = request.user

        if request.method == 'GET':
            rating = product.ratings.all()
            serializer = RatingSerializer(instance = rating, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('Ты уже поставил рейтинг на этот продукт',
                                status=400)
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)
        else:
            if not product.ratings.filter(owner=user).exists():
                return Response('Ты не можешь удалить, потому что ты не ставил рейтинг на этот продукт',
                                status=400)
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response('Удалено', status=204)











