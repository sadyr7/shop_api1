from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from product.models import Product
from category.models import Category
from product.views import ProductViewSet

User = get_user_model()

class ProductTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.access_token = self.setUp_user_token()
        self.setUp_category()
        self.setUp_product()

    def setUp_user(self):
        return User.objects.create_superuser('test@gmail.com', '1')

    def setUp_user_token(self):
        data = {
            'email': 'test@gmail.com',
            'password': '1'
        }

        request = self.factory.post('api/account/login/', data)
        view = TokenObtainPairView.as_view()
        response = view(request)
        return response.data['access']

    def setUp_product(self):
        products =[
            Product(owner=self.user, category=Category.objects.first(), price=20, image='image', title='test1', description='description1'),
            Product(owner=self.user, category=Category.objects.first(), price=20, image='image2', title='test2', description='description2'),
            Product(owner=self.user, category=Category.objects.first(), price=20, image='image3', title='test3', description='description3')
        ]
        Product.objects.bulk_create(products)

        def setUp_category(self):
            Category.objects.create(name='category1', slug='test_slug')


        def test_get_product(self):
            request = self.factory.get('/api/products/')
            view = ProductViewSet.as_view({'get': 'list'})
            response = view(request)

            assert response.status_code == 200
            assert Product.objects.count() == 3


        def test_post_product(self):
            image = open('avatars/Screenshot_from_2023-07-05_16-09-25_jI4o4wW.png')
            data = {
                'owner' : self.user.id,
                'category' : Category.objects.first().slug,
                'title': 'test_post',
                'price': 20,
                'image': image,
                'stock': 'in_stock',
                'description': 'description'
            }
            request = self.factory.post('/api/products/', data, HTTP_AUTHORIZATION='Bearer' + self.access_token)
            image.close()
            view = ProductViewSet.as_view({'post': 'create'})
            response = view(request)

            assert response.status_code == 201

