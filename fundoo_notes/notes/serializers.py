from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Note model.

    Meta:
        model (Note): The Note model to serialize.
        fields (list): List of fields to include in the serialized representation.
        read_only_fields (tuple): Fields that are read-only and cannot be modified.
    """
    class Meta:
        model = Note
        fields = [
            'id', 'title', 'description', 'color', 'image',
            'is_archive', 'is_trash', 'reminder', 'user'
        ]
        read_only_fields = ('user',)