   
from django.conf import settings
from django.db import models
from label.models import Label

class Note(models.Model):
    title = models.CharField(max_length=255, null=False, db_index=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='notes/images/', null=True, blank=True)
    is_archive = models.BooleanField(default=False, db_index=True)
    is_trash = models.BooleanField(default=False, db_index=True)
    reminder = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='notes')
    collaborator = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Collaborator' ,related_name='notes_collaborators') #collaborator
    label= models.ManyToManyField(Label, related_name='labels')
    class Meta:
        db_table = 'note'

class Collaborator(models.Model):
    READ_ONLY = 'read_only'
    READ_WRITE = 'read_write'

    ACCESS_TYPE_CHOICES = [
        (READ_ONLY, 'Read Only'),
        (READ_WRITE, 'Read and Write'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE,related_name='collaborators')
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPE_CHOICES,default=READ_ONLY)
    class Meta:
        unique_together = ('user', 'note')




