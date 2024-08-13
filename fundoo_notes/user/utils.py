
# from django.contrib.auth import authenticate
# fundoo_notes
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