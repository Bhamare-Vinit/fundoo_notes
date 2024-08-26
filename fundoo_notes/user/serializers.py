from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
import re

from django.contrib.auth import authenticate 
from rest_framework.exceptions import AuthenticationFailed

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_password(self, value):
        if not re.search(r"^(?=.*[!@#$%^&*()_+{}|:<>?])(?!.*[!@#$%^&*()_+{}|:<>?].*[!@#$%^&*()_+{}|:<>?]).*$", value):
            raise serializers.ValidationError("Password must contain at least one special character, one uppercase letter, one lowercase letter, and one digit.")
        return value
    
    def create(self, validated_data):
        # User.objects.create_user :hashes the password before storing 
        #User.objects.create : does not hashes password saves password as plain text thats why i used make_password method
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
        )
        return user

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = authenticate( email=validated_data['email'], password=validated_data['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return user
        