from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .serializers import NoteSerializer
from .models import Note
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)
User = get_user_model()
@shared_task(bind=True)
def send_reminder_email(self,title,description,email):
    """
    Send a reminder email.

    Parameters:
    - title (str): The title of the note.
    - description (str): The description of the note.
    - email (str): The recipient's email address.

    Return:
    - None
    """
    try:
        # note = Note.objects.get(id=note_id)
        # print(f"note = {note}")
        # print(f"note reminder= {note.reminder}")
        # serializer=NoteSerializer(note)
        # print(f"serializer.data = {serializer.data}")
        # note_data=serializer.data
        # print(f"note_data = {note_data}")
        # print(f"note_data reminder= {note_data['reminder']}")
        # print(f"type of reminder = {type(note_data['reminder'])}")
        # print(f"datetime now={timezone.now()} and its type ={type(timezone.now())}")
        # if note.reminder:
        #     #  and note.reminder >= timezone.now()
        #     print("inside if")
        #     user = User.objects.get(id=note_data['user'])
        subject = f"Reminder: {title}"
        message = f"Dear {email},\n\nThis is a reminder for your note: {title}.\n\n{description}"
        from_email='vinitbhamare2002@gmail.com'
        send_mail(subject, message, from_email, [email])
    # except Note.DoesNotExist:
    #     print("Note not found")
    # except User.DoesNotExist:
    #     print("User not found")
    except Exception as e:
        print(e)