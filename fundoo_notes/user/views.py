# from django.shortcuts import render
# import json
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.http import require_POST
# from user.models import User
# from django.forms.models import model_to_dict
# from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# import re
# import logging
# # Configure the logger
# logging.basicConfig(filename='user.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def check_if_valid_password(password):
#     try:
#         pattern = r"^(?=.*[!@#$%^&*()_+{}|:<>?])(?!.*[!@#$%^&*()_+{}|:<>?].*[!@#$%^&*()_+{}|:<>?]).*$"
#         if len(password) >= 8:
#             if re.search(r"[A-Z]", password) and re.search(r"\d", password) and re.search(r"[a-z]", password) and re.search(pattern, password):
#                 return True
#             else:
#                 logger.warning("Bad password: Missing required characters")
#                 return False
#         else:
#             logger.warning("Bad password: Too short")
#             return False
#     except Exception as e:
#         logger.error(f"Error validating password: {e}")
#         return False

# def check_if_valid_email(email):
#     try:
#         if re.search(r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?@[a-zA-Z0-9]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$", email):
#             return True
#         else:
#             logger.error(f"Error validating email: {e}")
#             return False
#     except Exception as e:
#         logger.error(f"Error validating email: {e}")
#         return False

# def check_if_valid_firstname_lastname(first_name, last_name):
#     try:
#         if re.search("[A-Z][a-z]{2,}$", first_name) and re.search("[A-Z][a-z]{2,}$", last_name):
#             return True
#         else:
#             logger.error(f"Error validating first name and last name: {e}")
#             return False
#     except Exception as e:
#         logger.error(f"Error validating first name and last name: {e}")
#         return False
    
# @require_POST
# def register_user(request):
#     if request.method=='POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({
#                 'message': 'Invalid JSON',
#                 'status': 'error'
#             }, status=400)

#         required_fields = ['first_name', 'last_name', 'email', 'password']
#         for field in required_fields:
#             if field not in data:
#                 return JsonResponse({
#                     'message': f'{field} is required',
#                     'status': 'error'
#                 }, status=400)
            
#         if check_if_valid_email(data['email']):
#             if check_if_valid_firstname_lastname(data['first_name'], data['last_name']):
#                 if check_if_valid_password(data['password']):
#                     try:
#                         User.objects.get(email=data['email'])
#                         return JsonResponse({
#                             'message': 'Email already exists',
#                             'status': 'error'
#                         }, status=400)
#                     except User.DoesNotExist:
#                         pass
#                     try:
#                         user = User.objects.create_user(
#                             first_name=data['first_name'],
#                             last_name=data['last_name'],
#                             email=data['email'],
#                             password=data['password']
#                         )
#                         user_dict = model_to_dict(user)
#                         specific_fields = {
#                             'first_name': user_dict.get('first_name'),
#                             'last_name': user_dict.get('last_name'),
#                             'email': user_dict.get('email')
#                         }

#                         return JsonResponse({
#                             'message': 'User registered successfully',
#                             'status': 'success',
#                             'data': specific_fields
#                         })
#                     except ValidationError as e:
#                         return JsonResponse({
#                             'message': 'Unexpected error occured',
#                             'status': 'error'
#                         }, status=400)

#                 else:
#                     return JsonResponse({
#                     'message': 'Invalid Password missing required characters',
#                     'status': 'error'
#                 }, status=400)
#             else:
#                 return JsonResponse({
#                 'message': 'Invalid first name or last name',
#                 'status': 'error'
#             }, status=400)

#         else:
#             return JsonResponse({
#                 'message': 'Invalid email',
#                 'status': 'error'
#             }, status=400)
#     else:
#         return HttpResponse("Invalid request method")
    
# @require_POST
# def login_user(request):
#     try:
#         data = json.loads(request.body)
#     except json.JSONDecodeError:
#         return JsonResponse({
#             'message': 'Invalid JSON',
#             'status': 'error'
#         }, status=400)

#     required_fields = ['email', 'password']
#     for field in required_fields:
#         if field not in data:
#             return JsonResponse({
#                 'message': f'{field} is required',
#                 'status': 'error'
#             }, status=400)

#     try:
#         # user = User.objects.get(email=data['email'])
#         user=authenticate(request, email=data['email'], password=data['password'])
#         if user:
#             # user_dict = model_to_dict(user)
#             specific_fields = {
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'email': user.email
#             }
#             return JsonResponse({
#                 'message': 'Login successful',
#                 'status': 'success',
#                 'data': specific_fields
#             })
#         else:
#             return JsonResponse({
#                 'message': 'Invalid credentials',
#                 'status': 'error'
#             }, status=401)
#     except Exception:
#         return JsonResponse({
#             'message': 'unexpected error occured',
#             'status': 'error'
#         }, status=404)

# # @require_POST
# # def login_user(request):
# #     try:
# #         data = json.loads(request.body)
# #     except json.JSONDecodeError:
# #         return JsonResponse({
# #             'message': 'Invalid JSON',
# #             'status': 'error'
# #         }, status=400)

# #     required_fields = ['email', 'password']
# #     for field in required_fields:
# #         if field not in data:
# #             return JsonResponse({
# #                 'message': f'{field} is required',
# #                 'status': 'error'
# #             }, status=400)

# #     try:
# #         user = User.objects.get(email=data['email'])
# #         if user.check_password(data['password']):
# #             user_dict = model_to_dict(user)
# #             specific_fields = {
# #                 'first_name': user_dict.get('first_name'),
# #                 'last_name': user_dict.get('last_name'),
# #                 'email': user_dict.get('email')
# #             }
# #             return JsonResponse({
# #                 'message': 'Login successful',
# #                 'status': 'success',
# #                 'data': specific_fields
# #             })
# #         else:
# #             return JsonResponse({
# #                 'message': 'Invalid password',
# #                 'status': 'error'
# #             }, status=401)
# #     except User.DoesNotExist:
# #         return JsonResponse({
# #             'message': 'User not found',
# #             'status': 'error'
# #         }, status=404)