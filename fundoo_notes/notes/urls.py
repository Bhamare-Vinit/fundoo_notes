
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet,CollaboratorViewSet,NoteLabelViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'labels', NoteLabelViewSet,basename='note-label')



urlpatterns = [
    path('', include(router.urls)),
]