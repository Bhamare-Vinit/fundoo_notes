from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id', 'title', 'description', 'color', 'image',
            'is_archive', 'is_trash', 'reminder', 'user'
        ]
        # Exclude 'user' from both input and output
        read_only_fields = ('user',)