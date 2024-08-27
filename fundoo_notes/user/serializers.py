from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
import re

from django.contrib.auth import authenticate 
from rest_framework.exceptions import AuthenticationFailed

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Description:
    Serializer for registering a new user. It validates the email for uniqueness
    and ensures the password meets the required criteria. The password is hashed before saving.

    Fields:
    - email: User's email address, must be unique.
    - password: User's password, must be at least 8 characters long and contain a special character.

    Methods:
    - validate_password(value): Validates that the password meets specific criteria.
    - create(validated_data): Creates a new user with the provided data, ensuring the password is hashed.
    """
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_password(self, value):
        """
        Description:
        Validates the password to ensure it contains at least one special character, 
        one uppercase letter, one lowercase letter, and one digit.

        Parameters:
        - value: The password entered by the user.

        Return:
        - The validated password if it meets the criteria.
        """
        if not re.search(r"^(?=.*[!@#$%^&*()_+{}|:<>?])(?!.*[!@#$%^&*()_+{}|:<>?].*[!@#$%^&*()_+{}|:<>?]).*$", value):
            raise serializers.ValidationError("Password must contain at least one special character, one uppercase letter, one lowercase letter, and one digit.")
        return value
    
    def create(self, validated_data):
        """
        Description:
        Creates a new user with hashed password.

        Parameters:
        - validated_data: The validated data containing user details.

        Return:
        - The created user instance.
        """
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
        """
        Meta options for UserRegistrationSerializer.

        Fields:
        - id: The user's ID.
        - first_name: The user's first name.
        - last_name: The user's last name.
        - email: The user's email address.
        - password: The user's password, write-only.
        """
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    """
    Description:
    Serializer for user login. It authenticates the user based on the provided email and password.

    Fields:
    - email: The user's email address.
    - password: The user's password, write-only.

    Methods:
    - create(validated_data): Authenticates the user with the provided credentials.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        Description:
        Authenticates the user using the provided email and password.

        Parameters:
        - validated_data: The validated data containing email and password.

        Return:
        - The authenticated user instance.
        """
        user = authenticate( email=validated_data['email'], password=validated_data['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return user
        