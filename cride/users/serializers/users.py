"""User Serializer"""

#Django
from django.conf import settings
from  django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

#DRF
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator



#Models
from cride.users.models import (
    User,
    Profile,
    )

#Utilities
from datetime import timedelta
import jwt

class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        """Meta class"""
        model = User
        fields = ('username',
                 'first_name',
                 'last_name',
                 'email',
                 'phone_number')


class UserSingupSerializer(serializers.Serializer):
    """User singup serializaer
    Handle sing up data validation and user/profile creation
    """
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        min_length=4, 
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    #password
    password = serializers.CharField(min_length=8, max_length=128)
    password_confirmation = serializers.CharField(min_length=8, max_length=128)

    #name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match")
        
        password_validation.validate_password(passwd)
        return data
    
    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user
    
    def send_confirmation_email(self, user):
        """Send account veification link to givin user."""
        verification_token = self.gen_verification_token(user)
        subject = "Welcome @{}! Verify your acoount start useing Comparte RIde"
        from_email ='Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'email/users/account_verication.html',
            {'token': verification_token, 'user': user}
            )
    
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
    
    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account."""
        exp_data =timezone.now() + timedelta(days=3)
        payload ={
            'user':user.username,
            'exp': int(exp_data.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    

class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer.
    Handle the login request data.
    Returns and validate the credentials.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def  validate(self,data):
        """Validate user credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data
    
    def create(self, data):
        """Generre or retriview new token."""
        token, user = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerficationSerializer(serializers.Serializer):
    """Account verification serializer"""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""

        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('invalid token')
        
        self.context['payload'] = payload
        return data
    
    def save(self):
        """Update user's verified status"""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()