from django.urls import path
from account.views import RegistrationView, ActivationView, LoginView, UserListView, RegistrationPhoneView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('register-phone/', RegistrationPhoneView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', UserListView.as_view())
]
