"""Users URLs."""

#Django
from django.urls import path
from cride.users.views import  (
    UserLoginAPIView,
    UserSingupViewPIView,)
urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('users/signup/', UserSingupViewPIView.as_view(), name="singup")
]