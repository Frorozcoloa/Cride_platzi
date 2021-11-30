"""Users URLs."""

#Django
from django.urls import path
from cride.users.views import  (
    UserLoginAPIView,
    UserSingupViewPIView,
    AccountVerficationAPIView)

urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('users/signup/', UserSingupViewPIView.as_view(), name="singup"),
    path('users/verify/', AccountVerficationAPIView.as_view(), name="verify"),
]