from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from .models import Label
from .serializers import LabelSerializer
from loguru import logger

class LabelView(
    generics.GenericAPIView, 
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin
):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # i used this function to assigne user fild with current logged in user
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation failed: {e.detail}")
            return Response({
                'error': 'Validation failed.',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred during label creation: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during creation.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            if 'pk' in kwargs:
                return self.retrieve(request, *args, **kwargs)
            return self.list(request, *args, **kwargs)
        except NotFound as e:
            logger.error(f"Label not found: {str(e)}")
            return Response({
                'error': 'Label not found.',
                'details': 'The label with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred while retrieving the label(s): {str(e)}")
            return Response({
                'error': 'An unexpected error occurred while retrieving the label(s).',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation failed: {e.detail}")
            return Response({
                'error': 'Validation failed.',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            logger.error(f"Label not found: {str(e)}")
            return Response({
                'error': 'Label not found.',
                'details': 'The label with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({
                'error': 'Permission denied.',
                'details': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"An error occurred while updating the label: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during the update.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation failed: {e.detail}")
            return Response({
                'error': 'Validation failed.',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            logger.error(f"Label not found: {str(e)}")
            return Response({
                'error': 'Label not found.',
                'details': 'The label with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({
                'error': 'Permission denied.',
                'details': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"An error occurred while partially updating the label: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during the partial update.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except NotFound as e:
            logger.error(f"Label not found: {str(e)}")
            return Response({
                'error': 'Label not found.',
                'details': 'The label with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({
                'error': 'Permission denied.',
                'details': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"An error occurred while deleting the label: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during deletion.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
