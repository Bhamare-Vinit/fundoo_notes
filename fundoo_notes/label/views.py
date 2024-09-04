from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from .models import Label
from .serializers import LabelSerializer
from loguru import logger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from django.db import connection
from .utils import dictfetchall
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
        


class RawLabelView(
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
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of labels filtered by the current user.
        """
        user_id = self.request.user.id
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM label WHERE user_id = %s", [user_id])
            labels=dictfetchall(cursor)

            # columns = [col[0] for col in cursor.description]
            # rows = cursor.fetchall()
            # labels = [dict(zip(columns, row)) for row in rows]
            
        return labels
    
    def perform_create(self, serializer):
        """
        Assigns the current user to the label and saves it.
        """
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Retrieves a label or a list of labels based on the request.
        """
        try:
            if 'pk' in kwargs:
                label_id = kwargs['pk']
                user_id = request.user.id
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM label WHERE id = %s AND user_id = %s", [label_id, user_id])
                    row = cursor.fetchone()
                    if not row:
                        raise NotFound("Label not found.")
                    label = Label(id=row[0], name=row[1], color=row[2], user_id=row[3])
                return Response(LabelSerializer(label).data)
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

    # def post(self, request, *args, **kwargs):
    #     """
    #     Creates a new label using the provided data.
    #     """
    #     try:
    #         data = request.data
    #         name = data.get('name')
    #         color = data.get('color', None)
    #         user_id = request.user.id

    #         if not name:
    #             raise ValidationError("The 'name' field is required.")

    #         with connection.cursor() as cursor:
    #             # Insert the new label and return the id
    #             cursor.execute(
    #                 "INSERT INTO label (name, color, user_id) VALUES (%s, %s, %s) RETURNING id",
    #                 [name, color, user_id]
    #             )
    #             label_id = cursor.fetchone()[0]

    #         with connection.cursor() as cursor:
    #             # Fetch the newly created label as a dictionary
    #             cursor.execute("SELECT * FROM label WHERE id = %s", [label_id])
    #             row = dictfetchall(cursor)
                
    #             if not row:
    #                 return Response({"error": "Label not found after creation."}, status=status.HTTP_404_NOT_FOUND)
                
    #             label_data = row[0]
    #             label_data['user'] = request.user

    #         return Response(LabelSerializer(label_data).data, status=status.HTTP_201_CREATED)

    #     except ValidationError as e:
    #         logger.error(f"Validation failed: {e.detail}")
    #         return Response({
    #             'error': 'Validation failed.',
    #             'details': e.detail
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         logger.error(f"An error occurred during label creation: {str(e)}")
    #         return Response({
    #             'error': 'An unexpected error occurred during creation.',
    #             'details': str(e)
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        """
        Creates a new label using the provided data, without using a serializer.
        """
        try:
            data = request.data
            name = data.get('name')
            color = data.get('color', None)
            user_id = request.user.id

            if not name:
                raise ValidationError("The 'name' field is required.")

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO label (name, color, user_id) VALUES (%s, %s, %s) RETURNING id",
                    [name, color, user_id]
                )
                label_id = cursor.fetchone()[0]#label id

            with connection.cursor() as cursor:
                #again fetch note just for displa output
                cursor.execute("SELECT * FROM label WHERE id = %s", [label_id])
                row = dictfetchall(cursor)
                
                if not row:
                    return Response({"error": "Label not found after creation."}, status=404)
                
                label_data = row[0]

            return Response(label_data, status=201)

        except ValidationError as e:
            logger.error(f"Validation failed: {e}")
            return Response({
                'error': 'Validation failed.',
                'details': str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"An error occurred during label creation: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during creation.',
                'details': str(e)
            }, status=500)

# https://docs.djangoproject.com/en/5.1/topics/db/sql/#executing-custom-sql-directly

class RawLabelView2(
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
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Label.objects.filter(user=self.request.user)
    def get_queryset(self):
        """
        Returns a queryset of labels filtered by the current user.
        """
        user_id = self.request.user.id
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM label WHERE user_id = %s", [user_id])
            labels=dictfetchall(cursor)
        return labels

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get(self, request, *args, **kwargs):
        """
        Retrieves a label or a list of labels based on the request.
        """
        try:
            if 'pk' in kwargs:
                label_id = kwargs['pk']
                user_id = request.user.id
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM label WHERE id = %s AND user_id = %s", [label_id, user_id])
                    row = cursor.fetchone()
                    if not row:
                        raise NotFound("Label not found.")
                    label = Label(id=row[0], name=row[1], color=row[2], user_id=row[3])
                return Response(LabelSerializer(label).data)
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
        """
        Updates an existing label using the provided data, without using a serializer.
        """
        try:
            label_id = kwargs.get('pk')
            data = request.data
            name = data.get('name', None)
            color = data.get('color', None)
            user_id = request.user.id

            if not name:
                raise ValidationError("The 'name' field is required.")

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM label WHERE id = %s AND user_id = %s", [label_id, user_id])
                row = cursor.fetchone()
                if not row:
                    return Response({"error": "Label not found."}, status=404)

                cursor.execute(
                    "UPDATE label SET name = %s, color = %s WHERE id = %s AND user_id = %s",
                    [name, color, label_id, user_id]
                )
                cursor.execute("SELECT * FROM label WHERE id = %s", [label_id])
                updated_label = dictfetchall(cursor)

            return Response(updated_label, status=200)

        except ValidationError as e:
            logger.error(f"Validation failed: {e}")
            return Response({
                'error': 'Validation failed.',
                'details': str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"An error occurred during label update: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during the update.',
                'details': str(e)
            }, status=500)

    # def put(self, request, *args, **kwargs):
    #     """
    #     Updates an existing label using the provided data, without using a serializer.
    #     """
    #     try:
    #         label_id = kwargs.get('pk')
    #         data = request.data
    #         name = data.get('name', None)
    #         color = data.get('color', None)
    #         user_id = request.user.id

    #         if not name:
    #             return Response({"error": "The 'name' field is required."}, status=400)

    #         with connection.cursor() as cursor:
    #             # Check if the label exists and belongs to the user
    #             cursor.execute("SELECT * FROM label WHERE id = %s AND user_id = %s", [label_id, user_id])
    #             row = cursor.fetchone()
    #             if not row:
    #                 return Response({"error": "Label not found."}, status=404)

    #             # Update the label in the database
    #             cursor.execute(
    #                 "UPDATE label SET name = %s, color = %s WHERE id = %s AND user_id = %s",
    #                 [name, color, label_id, user_id]
    #             )

    #             # Fetch the updated label
    #             cursor.execute("SELECT * FROM label WHERE id = %s", [label_id])
    #             updated_label = dictfetchall(cursor)

    #         return Response(updated_label, status=200)

    #     except ValidationError as e:
    #         logger.error(f"Validation failed: {e}")
    #         return Response({
    #             'error': 'Validation failed.',
    #             'details': str(e)
    #         }, status=400)
    #     except Exception as e:
    #         logger.error(f"An error occurred during label update: {str(e)}")
    #         return Response({
    #             'error': 'An unexpected error occurred during the update.',
    #             'details': str(e)
    #         }, status=500)
    def delete(self, request, *args, **kwargs):
        """
        Deletes an existing label by ID.
        """
        try:
            label_id = kwargs.get('pk')
            user_id = request.user.id

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM label WHERE id = %s AND user_id = %s", [label_id, user_id])
                row = cursor.fetchone()
                if not row:
                    return Response({"error": "Label not found."}, status=404)
                cursor.execute("DELETE FROM label WHERE id = %s AND user_id = %s", [label_id, user_id])

            return Response({"message": "Label deleted successfully."}, status=204)

        except Exception as e:
            logger.error(f"An error occurred during label deletion: {str(e)}")
            return Response({
                'error': 'An unexpected error occurred during deletion.',
                'details': str(e)
            }, status=500)

