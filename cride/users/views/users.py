"""Users views."""

#DRF
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSingupSerializer,)


class UserLoginAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        """Handle the login"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data ={
            'user':UserModelSerializer(user).data,
            "acces_token": token
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

class UserSingupViewPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        """Handle the login"""
        serializer = UserSingupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data =UserModelSerializer(user).data

        return Response(data=data, status=status.HTTP_201_CREATED)