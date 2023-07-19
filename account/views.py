from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView, View
from rest_framework.response import Response

from account.send_email import send_confirmation_email
from account.serializers import RegisterSerializer, ActivationSerializer
User = get_user_model()


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email(user.email,
                                        user.activation_code)
            except:
                return Response({'message': 'Зарегистрировался, но на почту код не отправился'
                                 ,'data': serializer.data}, status=201)

        return Response(serializer.data, status=201)


# 1 вариант
# class ActivationView(GenericAPIView):
#     serializer_class = ActivationSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data = request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response('Успешно активирован', status=200)

# 2 вариант
class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User,  activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Успешно активирован', status=200)
#



