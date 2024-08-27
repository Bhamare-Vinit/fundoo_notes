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
from .utils.redis_utils import RedisUtils
import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import localtime
from .tasks import send_reminder_email
from drf_yasg.utils import swagger_auto_schema

class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Note instances with caching and task scheduling.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes=[]
    redis=RedisUtils()

    def get_queryset(self):

        return Note.objects.filter(user=self.request.user)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        List all notes for the current user.

        Parameters:
        - request: The HTTP request object.

        Return:
        - Response: JSON response with list of notes.
        """
        try:
            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)

            if cached_notes:

                filtered_notes = [
                    note for note in cached_notes
                    if not note['is_archive'] and not note['is_trash']
                ]

                return Response({
                    "message": "Notes retrieved from cache.",
                    "data": filtered_notes
                }, status=status.HTTP_200_OK)

            notes = self.get_queryset()
            serializer = self.get_serializer(notes, many=True)

            self.redis.save(cache_key, serializer.data, ex=3600)

            filtered_notes = [
                note for note in serializer.data
                if not note['is_archive'] and not note['is_trash']
            ]

            return Response({
                "message": "Notes retrieved successfully.",
                "data": filtered_notes
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in list method: {e}")
            return Response({
                "error": "An error occurred while retrieving notes.",
                "detail": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(operation_description="Creation of note",request_body=NoteSerializer, responses={201: NoteSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def create(self, request, *args, **kwargs):
        """
        Create a new note and schedule reminder tasks.

        Parameters:
        - request: The HTTP request object with note data.

        Return:
        - Response: JSON response with created note details.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            note=serializer.save(user=request.user)
            print(f"note={note}")

            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)

            if cached_notes:
                cached_notes.append(serializer.data)
                self.redis.save(cache_key, cached_notes, ex=3600)
            else:
                self.redis.save(cache_key, [serializer.data], ex=3600)
            print(f"note:{note}, type={type(note)}")
            print(f"note.reminder = {note.reminder}")
            print(f"note.id ={note.id}")

            if note.reminder:
                reminder_time = note.reminder
                schedule, created = CrontabSchedule.objects.get_or_create(
                    minute=str(reminder_time.minute),
                    hour=str(reminder_time.hour),
                    day_of_month=str(reminder_time.day),
                    month_of_year=str(reminder_time.month),
                    day_of_week='*',
                )
                PeriodicTask.objects.create(
                    crontab=schedule,
                    name=f"send_reminder_email_{note.id}",
                    task='notes.tasks.send_reminder_email',
                    args=json.dumps([note.title,note.description,note.user.email]),
                )
            headers = self.get_success_headers(serializer.data)
            return Response({
                "message": "Note created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            logger.error(f"Error in create method: {e}")
            return Response({
                "error": "An error occurred while creating the note.",
                "detail": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a specific note by ID.

        Parameters:
        - request: The HTTP request object.
        - pk: The ID of the note to retrieve.

        Return:
        - Response: JSON response with note details.
        """
        try:
            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)
            print(f"cached_notes: {cached_notes}")

            if cached_notes:
                for note in cached_notes:
                    if note['id'] == int(pk):
                        print(f"note: {note}")
                        return Response({
                            'user': request.user.email,
                            'message': 'Note retrieved successfully from cache.',
                            'data': note
                        }, status=status.HTTP_200_OK)
                
                logger.error(f"Note with ID: {pk} not found in cache for user: {request.user.email}")
                return Response({
                    'user': request.user.email,
                    'error': 'Note not found in cache.',
                    'detail': f'The note with ID {pk} does not exist in the cache.'
                }, status=status.HTTP_404_NOT_FOUND)

            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            all_notes = self.get_serializer(self.get_queryset(), many=True).data
            self.redis.save(cache_key, all_notes, ex=3600)

            return Response({
                'user': request.user.email,
                'message': 'Note retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except NotFound:
            logger.error(f"Note with ID: {pk} not found for user: {request.user.email}")
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred while retrieving note with ID: {pk} for user: {request.user.email}. Error: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while retrieving the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Creation of note",request_body=NoteSerializer, responses={201: NoteSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def update(self, request, *args, **kwargs):
        """
        Update an existing note.

        Parameters:
        - request: The HTTP request object with updated note data.

        Return:
        - Response: JSON response with updated note details.
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            note=serializer.save()

            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)

            if cached_notes:
                for index, note in enumerate(cached_notes):
                    if note['id'] == instance.id:
                        cached_notes[index] = serializer.data
                        print("cache updated")
                        break

                self.redis.save(cache_key, cached_notes, ex=3600)
            print("good till now")
            print("note.reminder = note",instance.reminder)
            if instance.reminder:

            # Delete the old periodic task
                update_task=PeriodicTask.objects.filter(name=f"send_reminder_email_{instance.id}")
            
                # Create or update the CrontabSchedule
                schedule, created = CrontabSchedule.objects.get_or_create(
                    minute=instance.reminder.minute,
                    hour=instance.reminder.hour,
                    day_of_month=instance.reminder.day,
                    month_of_year=instance.reminder.month,
                    day_of_week='*',
                )
                if not update_task.exists():
                    print("nhi he")
                    PeriodicTask.objects.create(
                        crontab=schedule,
                        name=f"send_reminder_email_{instance.id}",
                        task='notes.tasks.send_reminder_email',
                        args=json.dumps([instance.title,instance.description,instance.user.email]),
                    )
                else:
                    print("kuchh to ho000000")
                    update_task = update_task.first()
                    # update_task.update(crontab=schedule)
                    # update_task.schedule = schedule
                    # update_task.save()
                    update_task.crontab = schedule
                    update_task.save()
            headers = self.get_success_headers(serializer.data)
            return Response({
                'user': request.user.email,
                'message': 'Note updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK, headers=headers)
        except ValidationError as e:
            logger.error("Validation failed for user: {}. Error: {}", request.user.email, e.detail)
            return Response({
                'user': request.user.email,
                'error': 'Validation failed.',
                'detail': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred while updating the note for user: {}. Error: {}", request.user.email, str(e))
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while updating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

 
    @swagger_auto_schema(operation_description="Creation of note",request_body=NoteSerializer, responses={201: NoteSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete a note by ID.

        Parameters:
        - request: The HTTP request object.
        - pk: The ID of the note to delete.

        Return:
        - Response: Confirmation of deletion.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)

            if cached_notes:
                updated_cache_notes = []
                for note in cached_notes:
                    if note['id'] != int(pk):
                        updated_cache_notes.append(note)
                        print(f"Cache Updated: {updated_cache_notes}")
                
                self.redis.save(cache_key, updated_cache_notes, ex=3600)

            return Response({
                'user': request.user.email,
                'message': 'Note deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except NotFound:
            logger.error(f"Note with ID {pk} not found for user {request.user.email}.")
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred while deleting note with ID {pk} for user {request.user.email}: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while deleting the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(operation_description="Creation of note",request_body=NoteSerializer, responses={201: NoteSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    @action(detail=True, methods=['patch'], url_path='toggle_archive', permission_classes=[IsAuthenticated])
    def toggle_archive(self, request, pk=None):
        """
        Toggle the archive status of a note.

        Parameters:
        - request: The HTTP request object.
        - pk: The ID of the note to update.

        Return:
        - Response: JSON response with updated note details.
        """
        try:
            note = self.get_object()

            note.is_archive = not note.is_archive
            note.save()

            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)
            print(f"cashed toggle:{cached_notes}")

            if cached_notes:
                for cached_note in cached_notes:
                    if cached_note['id'] == note.id:
                        cached_note['is_archive'] = note.is_archive
                        print("cache updated toggle archive")
                        break
                self.redis.save(cache_key, cached_notes, ex=3600)

            return Response({
                'user': request.user.email,
                'message': 'Note archive status toggled successfully.',
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
            logger.error(f"An error occurred while toggling archive status for note with ID {pk} for user {request.user.email}: {str(e)}")
            return Response({
                'user': request.user.email,
                'error': 'An error occurred while toggling the archive status.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
  
    @action(detail=False, methods=['get'], url_path='archived_notes', permission_classes=[IsAuthenticated])
    def archived_notes(self, request):
        """
        List all archived notes for the current user.

        Parameters:
        - request: The HTTP request object.

        Return:
        - Response: JSON response with archived notes.
        """
        try:
            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)
            print(f"Archived Notes:{cached_notes}")

            if cached_notes:
                archived_notes = [note for note in cached_notes if note.get('is_archive', False)]
                print(f"aechived notes:{archived_notes}")
                return Response({
                    'user': request.user.email,
                    'message': 'Archived notes retrieved successfully from cache.',
                    'data': archived_notes
                }, status=status.HTTP_200_OK)
            
            queryset = Note.objects.filter(user=request.user, is_archive=True)
            serializer = self.get_serializer(queryset, many=True)
            self.redis.save(cache_key, serializer.data, ex=3600)
            
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
    @swagger_auto_schema(operation_description="Creation of note",request_body=NoteSerializer, responses={201: NoteSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})    
    @action(detail=True, methods=['patch'], url_path='toggle_trash', permission_classes=[IsAuthenticated])
    def toggle_trash(self, request, pk=None):
        """
        Toggle the trash status of a note.

        Parameters:
        - request: The HTTP request object.
        - pk: The ID of the note to update.

        Return:
        - Response: JSON response with updated note details.
        """
        try:
            note = self.get_object()
            note.is_trash = not note.is_trash
            note.save()

            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)

            if cached_notes:
                updated_note_data = NoteSerializer(note).data
                updated_notes = [
                    updated_note_data if n['id'] == note.id else n
                    for n in cached_notes
                ]
                self.redis.save(cache_key, updated_notes, ex=3600)
                print("Toggle trash")
            else:
                queryset = self.get_queryset().filter(is_archive=False, is_trash=False)
                self.redis.save(cache_key, self.get_serializer(queryset, many=True).data, ex=300)

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
        """
        List all trashed notes for the current user.

        Parameters:
        - request: The HTTP request object.

        Return:
        - Response: JSON response with trashed notes.
        """
        try:
            cache_key = f"user_{request.user.id}"
            cached_notes = self.redis.get(cache_key)

            if cached_notes:
                
                trashed_notes = [note for note in cached_notes if note.get('is_trash', False)]
                return Response({
                    'user': request.user.email,
                    'message': 'Trashed notes retrieved successfully from cache.',
                    'data': trashed_notes
                }, status=status.HTTP_200_OK)
            
            queryset = self.get_queryset().filter(is_trash=True)
            serializer = self.get_serializer(queryset, many=True)

            self.redis.save(cache_key, serializer.data, ex=3600)
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
    


