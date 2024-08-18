# # notes/views.py
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Note
# from .serializers import NoteSerializer
# from rest_framework.permissions import IsAuthenticated

# class NoteViewSet(viewsets.ModelViewSet):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     # permission_classes = [IsAuthenticated]

#     # authentication_classes=[]

#     def get_queryset(self):
#         return Note.objects.filter(user=self.request.user)
    
#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().filter(is_archive=False,is_trash=False)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # self.perform_create(serializer)
#         serializer.save(user=request.user)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def retrieve(self, request, pk=None, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def update(self, request, pk=None, *args, **kwargs):
#         partial = False
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def partial_update(self, request, pk=None, *args, **kwargs):
#         partial = True
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def destroy(self, request, pk=None, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from django.core.exceptions import PermissionDenied

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
            return Response({
                'user': request.user.email,
                'error': 'Validation failed.',
                'detail': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
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
            return Response({
                'user': request.user.email,
                'error': 'Note not found.',
                'detail': 'The note with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
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

