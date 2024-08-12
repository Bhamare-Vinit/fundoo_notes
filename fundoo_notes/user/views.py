from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from user.models import User
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError


@require_POST
def register_user(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'message': 'Invalid JSON',
            'status': 'error'
        }, status=400)

    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in request_data:
            return JsonResponse({
                'message': f'{field} is required',
                'status': 'error'
            }, status=400)

    # Validate email
    try:
        User.objects.get(email=request_data['email'])
        return JsonResponse({
            'message': 'Email already exists',
            'status': 'error'
        }, status=400)
    except User.DoesNotExist:
        pass

    # Create user
    try:
        user = User.objects.create_user(
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            email=request_data['email'],
            password=request_data['password']
        )
        user_dict = model_to_dict(user)
        specific_fields = {
            'first_name': user_dict.get('first_name'),
            'last_name': user_dict.get('last_name'),
            'email': user_dict.get('email')
        }

        return JsonResponse({
            'message': 'User registered successfully',
            'status': 'success',
            'data': specific_fields
        })
    except ValidationError as e:
        return JsonResponse({
            'message': 'Unexpected error occured',
            'status': 'error'
        }, status=400)
