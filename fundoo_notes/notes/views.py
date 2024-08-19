from loguru import logger
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError,PermissionDenied
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # permission_classes = [IsAuthenticated]

    # authentication_classes=[]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().filter(is_archive=False, is_trash=False)
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'user': request.user.email,
                'message': 'Notes retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in list method: {e}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while retrieving notes.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # self.perform_create(serializer)
            serializer.save(user=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'user': request.user.email,
                'message': 'Note created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.error("Validation failed for user: {}. Error: {}", request.user.email, e.detail)
            return Response({
                'user': request.user.email,
                'error': 'Validation failed.',
                'detail': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred while creating the note for user: {}. Error: {}", request.user.email, str(e))
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while creating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'user': request.user.email,
                'message': 'Note retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except NotFound:
            logger.error("Note with ID: {} not found for user: {}", pk, request.user.email)
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("An error occurred while retrieving note with ID: {} for user: {}. Error: {}", pk, request.user.email, str(e))
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while retrieving the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        partial = False
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'user': request.user.email,
                'message': 'Note updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Validation failed: {e.detail}")
            return Response({
                'user': request.user.email,
                'error': 'Validation failed.',
                'detail': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            logger.error(f"Note not found for user: {request.user.email}")
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'Permission denied.',
                'detail': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"An error occurred while updating the note: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while updating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        partial = True
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'user': request.user.email,
                'message': 'Note partially updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                'user': request.user.email,
                'error': 'Validation failed.',
                'detail': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({
                'user': request.user.email,
                'error': 'Permission denied.',
                'detail': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while partially updating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'user': request.user.email,
                'message': 'Note deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({
                'user': request.user.email,
                'error': 'Permission denied.',
                'detail': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while deleting the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['patch'], url_path='toggle_archive', permission_classes=[IsAuthenticated])
    def toggle_archive(self, request, pk=None):
        try:
            note = self.get_object()
            note.is_archive = not note.is_archive
            note.save()
            return Response({
                'user': request.user.email,
                'message': 'Note archive status toggled successfully.',
                'data': NoteSerializer(note).data
            }, status=status.HTTP_200_OK)
        except NotFound:
            logger.error(f"Note not found for user: {request.user.email}")
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred while deleting the note: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while toggling the archive status.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], url_path='archived_notes', permission_classes=[IsAuthenticated])
    def archived_notes(self, request):
        try:
            queryset = Note.objects.filter(user=request.user, is_archive=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'user': request.user.email,
                'message': 'Archived notes retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred while retrieving archived notes for user {request.user.email}: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while retrieving archived notes.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['patch'], url_path='toggle_trash', permission_classes=[IsAuthenticated])
    def toggle_trash(self, request, pk=None):
        try:
            note = self.get_object()
            note.is_trash = not note.is_trash
            note.save()
            return Response({
                'user': request.user.email,
                'message': 'Note trash status toggled successfully.',
                'data': NoteSerializer(note).data
            }, status=status.HTTP_200_OK)
        except NotFound:
            logger.error(f"Note with ID {pk} not found for user {request.user.email}.")
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred while toggling trash status for note with ID {pk} for user {request.user.email}: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while toggling the trash status.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], url_path='trashed_notes')
    def trashed_notes(self, request):
        try:
            queryset = Note.objects.filter(user=request.user, is_trash=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'user': request.user.email,
                'message': 'Trashed notes retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred while retrieving trashed notes for user {request.user.email}: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while retrieving trashed notes.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    


