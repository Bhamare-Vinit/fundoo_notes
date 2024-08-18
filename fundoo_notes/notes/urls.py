
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# {
#     "message": "Registration successful",
#     "data": {
#         "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMzkxNzg0OCwiaWF0IjoxNzIzODMxNDQ4LCJqdGkiOiIyZTE1YzU0ZWEzN2I0YzNhYTkzNzVlNzdmY2RiMzM0MyIsInVzZXJfaWQiOjI1fQ.0qpVgThlEDMvvvUYwwqPr0R8GE5BPUpjdja7osNEdak",
#         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzODM1MDQ4LCJpYXQiOjE3MjM4MzE0NDgsImp0aSI6ImVmOWM5YTk5MTQ5NzQ4OGM4ZGYzYjRiZTgzMmUxOWY0IiwidXNlcl9pZCI6MjV9.YVY0oLbFm_r9fdnR2jJ2aUg6ituEvRmHV3hWtJB2F3c"
#     }
# }


# {
#     "message": "Login successful",
#     "data": {
#         "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMzkxNzk0OSwiaWF0IjoxNzIzODMxNTQ5LCJqdGkiOiJmMzEzNWU2Y2I0YTg0ZmUxYTY1MGYwODc2NmVmN2ZhZSIsInVzZXJfaWQiOjI1fQ.9cz62501XUz65jOXwDMenVFecTuKXx4rlpnlpz0iv7M",
#         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzODM1MTQ5LCJpYXQiOjE3MjM4MzE1NDksImp0aSI6IjlmMzMxYjg1YWRhMDQ5YTI5MTE0NDVmZTJmMzhjY2U4IiwidXNlcl9pZCI6MjV9.uT-7jmLnEp2WHulfYeJKXwGJzlsJvtLZcsrUpswE_j8"
#     }
# }