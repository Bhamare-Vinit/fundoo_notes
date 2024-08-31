from rest_framework import serializers
from .models import Note,Collaborator
from label.models import Label
class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Note model.

    Meta:
        model (Note): The Note model to serialize.
        fields (list): List of fields to include in the serialized representation.
        read_only_fields (tuple): Fields that are read-only and cannot be modified.
    """
    # label = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = [
            'id',
              'title', 'description', 'color', 'image',
            'is_archive', 'is_trash', 'reminder', 
            'user','label','collaborator'
        ]
        read_only_fields = ('user','label','collaborator')
    
class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = ['access_type', 'note', 'user']