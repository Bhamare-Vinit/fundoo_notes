from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.reverse import reverse
from django.conf import settings
import jwt
from .tasks import send_verification_email
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import Throttled

class UserLoginView(APIView):
    """
    Description:
    Handles user login by validating credentials and returning a JWT token if successful.

    Parameters:
    - request: Contains user credentials (email and password).

    Return:
    - A success response with user data and a JWT token.
    - An error response if login fails or an exception occurs.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]
    @swagger_auto_schema(operation_description="user login",request_body=UserLoginSerializer, responses={200: UserLoginSerializer})
    
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            # if user:
            user = serializer.save()
            if not user.is_verified:
                return Response({"error": "User is not verified. Please verify your email to log in."}, status=status.HTTP_403_FORBIDDEN)
            token=RefreshToken.for_user(serializer.instance)
            user_data = {
                'email': serializer.instance.email,
                'first_name': serializer.instance.first_name,
                'last_name': serializer.instance.last_name,
                'access': str(token.access_token)
            }
            return Response({'message': 'Login successful','data':user_data,'status': 'success',}, status=status.HTTP_200_OK)
        #'refresh': str(token), 'access': str(token.access_token)
                # return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response(
                {
                    'message': str(e),
                    'status': 'error',
                    'data': {}
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Throttled as e:
            return Response({"error": "You have exceeded your request limit. Please try again later.",'data': {'error': str(e)}}, status=429)
        except Exception as e:
            return Response(
                {
                    'message': 'An error occurred',
                    'status': 'error',
                    'data': {'error': str(e)}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

from .tasks import send_verification_email
class UserRegistrationView(APIView):
    """
    Description:
    Handles user registration, saves the user's data, and sends a verification email.

    Parameters:
    - request: Contains user registration details.

    Return:
    - A success response with user data if registration is successful.
    - An error response if registration fails or an exception occurs.
    """
    authentication_classes = []  # no authentication
    permission_classes = [AllowAny]
    @swagger_auto_schema(operation_description="user register",request_body=UserRegistrationSerializer, responses={201: UserRegistrationSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})

    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                token=RefreshToken.for_user(serializer.instance)
                link=reverse('verify', args=[str(token.access_token)],request=request)
                subject="Welcome to fundoo notes"
                message=f"Hi {serializer.data['first_name']} {serializer.data['last_name']}, thank you for registering.\n Click:\n{link}"
                from_email='vinitbhamare2002@gmail.com'
                to_email=serializer.data['email']
                send_verification_email.delay(subject, message,from_email , to_email)
                # return Response({'message': 'Registration successful','data':{'refresh': str(token), 'access': str(token.access_token)}}, status=status.HTTP_201_CREATED)
                # user_data = {
                #     'email': serializer.data['email'],
                #     'first_name': serializer.data['first_name'],
                #     'last_name': serializer.data['last_name'],
                #     # 'access': str(token.access_token)
                # }

                return Response(
                    {
                        'message': 'Registration successful',
                        'status': 'success',
                        'data':serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(
                {
                    'message': 'Validation failed',
                    'status': 'error',
                    'data': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    'message': 'An error occurred during registration',
                    'status': 'error',
                    'data': {'error': str(e)}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(["GET"])
@permission_classes([AllowAny])#dont comment this line again

def verify_registered_user(request, token):
    """
    Description:
    Verifies a user's account by decoding the JWT token and marking the user as verified.

    Parameters:
    - request: The HTTP request object.
    - token: The JWT token for user verification.

    Return:
    - A success response if the token is valid.
    - An error response if the token is invalid or expired.
    """
    try:
        decoded_token = AccessToken(token)
        print(f"token decoded: {decoded_token}")

        # payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
        user=User.objects.get(id=decoded_token['user_id'])
        user.is_verified=True
        user.save()
        return Response({
            'message': 'Token decoded successfully',
            'decoded_token': decoded_token.payload
        }, status=200)
    
    except InvalidToken as e:
        return Response({
            'error': 'Invalid token',
            'details': str(e)
        }, status=400)
    except TokenError:
        return Response({
            'error': 'Token error or expired'
        }, status=400)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 


# # Create your views here.
# # Home page
# def index(request):
#     return render(request, 'index.html')

# # signup page
# def user_signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login_page')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

# # login page
# # def user_login(request):
# #     if request.method == 'POST':
# #         form = LoginForm(request.POST)
# #         if form.is_valid():
# #             username = form.cleaned_data['username']
# #             password = form.cleaned_data['password']
# #             user = authenticate(request, username=username, password=password)
# #             if user:
# #                 login(request, user)    
# #                 return redirect('home')
# #     else:
# #         form = LoginForm()
# #     return render(request, 'login.html', {'form': form})
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form.add_error(None, "Invalid email or password")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# # logout page
# def user_logout(request):
#     logout(request)
#     return redirect('login_page')

from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from .models import User
from django.shortcuts import render, redirect

def user_signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        return redirect('login_page')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('profile')
    return render(request, 'login.html')

from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    return render(request, 'index.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('login_page')