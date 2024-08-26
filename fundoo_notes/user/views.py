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

class UserLoginView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
                # user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
                # if user:
            serializer.save()
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
    authentication_classes = []  # no authentication
    permission_classes = [AllowAny]
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
@permission_classes([AllowAny])
def verify_registered_user(request, token):
    try:
        decoded_token = AccessToken(token)
        print(decoded_token)

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