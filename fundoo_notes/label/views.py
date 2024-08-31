from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from .models import Label
from .serializers import LabelSerializer
from loguru import logger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed

class LabelView(
    generics.GenericAPIView, 
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin
):
    """
    API view for managing Label objects with CRUD operations.
    """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Description:
            Returns a queryset of labels filtered by the current user.

        Parameter:
            None

        Return:
            Queryset of Label objects for the current user.
        """
        return Label.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Description:
            Assigns the current user to the label and saves it.

        Parameter:
            serializer (LabelSerializer): The serializer instance used to save the label.

        Return:
            None
        """
        # i used this function to assigne user fild with current logged in user
        serializer.save(user=self.request.user)
    @swagger_auto_schema(operation_description="Creation of note",request_body=LabelSerializer, responses={201: LabelSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def post(self, request, *args, **kwargs):
        """
        Description:
            Creates a new label using the provided data.

        Parameter:
            request (Request): The HTTP request containing the label data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            Response: The response with the created label or error details.
        """
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
        """
        Description:
            Retrieves a label or a list of labels based on the request.

        Parameter:
            request (Request): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            Response: The response with the label(s) or error details.
        """
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
        
    


class LabelView2(
    generics.GenericAPIView, 
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin
):
    """
    API view for managing Label objects with CRUD operations.
    """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Description:
            Returns a queryset of labels filtered by the current user.

        Parameter:
            None

        Return:
            Queryset of Label objects for the current user.
        """
        return Label.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Description:
            Assigns the current user to the label and saves it.

        Parameter:
            serializer (LabelSerializer): The serializer instance used to save the label.

        Return:
            None
        """
        # i used this function to assigne user fild with current logged in user
        serializer.save(user=self.request.user)
    
    @swagger_auto_schema(operation_description="Creation of note",request_body=LabelSerializer, responses={201: LabelSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def put(self, request, *args, **kwargs):
        """
        Description:
            Updates an existing label with the provided data.

        Parameter:
            request (Request): The HTTP request containing the update data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            Response: The response with the updated label or error details.
        """
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
    @swagger_auto_schema(operation_description="Creation of note",request_body=LabelSerializer, responses={201: LabelSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def patch(self, request, *args, **kwargs):
        """
        Description:
            Partially updates an existing label with the provided data.

        Parameter:
            request (Request): The HTTP request containing the partial update data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            Response: The response with the partially updated label or error details.
        """
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
        

    @swagger_auto_schema(operation_description="Creation of note",request_body=LabelSerializer, responses={201: LabelSerializer,400: "Bad Request: Invalid input data.",
            500: "Internal Server Error: An error occurred during registration."})
    def delete(self, request, *args, **kwargs):
        """
        Description:
            Deletes a label based on the provided ID.

        Parameter:
            request (Request): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            Response: The response with the result of the deletion or error details.
        """
        try:
            return self.destroy(request, *args, **kwargs)
        
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response(
                {
                    'error': 'Permission denied.',
                    'details': str(e)
                },
                status=status.HTTP_403_FORBIDDEN
            )
        except NotFound as e:
            logger.error(f"Label not found: {str(e)}")
            return Response({
                'error': 'Label not found.',
                'details': 'The label with the provided ID does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            logger.error(f"Validation failed: {e.detail}")
            return Response({
                'error': 'Validation failed.',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            logger.error(f"Authentication failed: {str(e)}")
            return Response(
                {
                    'error': 'Authentication failed.',
                    'details': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        

        # except Exception as e:
        #     logger.error(f"An error occurred while deleting the label: {str(e)}")
        #     return Response({
        #         'error': 'An unexpected error occurred during deletion.',
        #         'details': str(e)
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, *args, **kwargs):
        """
        Description:
            Retrieves a label or a list of labels based on the request.

        Parameter:
            request (Request): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            Response: The response with the label(s) or error details.
        """
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

