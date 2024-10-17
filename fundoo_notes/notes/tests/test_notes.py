import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status

@pytest.fixture
def generate_usertoken(client, django_user_model):
    django_user_model.objects.create_user(
        first_name="Vinit",
        last_name="Bhmare",
        email="ombhamare2001@gmail.com",
        password="Vinit@2002",
        is_verified=True
    )
    data = {
        "email": "ombhamare2001@gmail.com",
        "password": "Vinit@2002"
    }
    url = reverse('login')
    response = client.post(url, data=data, content_type='application/json')
    return response.data["data"]["access"]

@pytest.fixture
def get_id(client, django_user_model):
    django_user_model.objects.create_user(
        first_name="Vinit",
        last_name="Bhmare",
        email="ombhamare2001@gmail.com",
        password="Vinit@2002",
        is_verified=True
    )
    data = {
        "email": "ombhamare2001@gmail.com",
        "password": "Vinit@2002"
    }
    url = reverse('login')
    response = client.post(url, data=data, content_type='application/json')
    return response.data["data"]["id"]

@pytest.fixture
def generate_usertoken2(client, django_user_model):
    django_user_model.objects.create_user(
        first_name="Vinit",
        last_name="Bhmare",
        email="abhibhamare2001@gmail.com",
        password="Vinit@2002",
        is_verified=True
    )
    data = {
        "email": "abhibhamare2001@gmail.com",
        "password": "Vinit@2002"
    }
    url = reverse('login')
    response = client.post(url, data=data, content_type='application/json')
    return response.data["data"]["access"]

@pytest.mark.django_db
@pytest.mark.note
class TestNote:
#-------------------------Create Note--------------------------------------------------------------
    def test_note_create(self,client,generate_usertoken):
        data = {
            "title": "Meeting",
            "description": "This is the description of my secret note.",
            "color": "violet",
            "is_archive": True,
            "is_trash": False,
            "reminder":"2024-08-26T11:50"
        }
        url = reverse('notes-list')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',data=data,content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print(response.data["data"])
        return response.data["data"]["id"]
    
    def test_add_note_unauthenticated(self,client):  
        note_data = {
            "title": "Test Note",
            "description": "This is a test note.",
            "color": "blue",
            "is_archive": False,
            "is_trash": False,
            "reminder": "2024-08-29T12:00:00Z"
        }
        url = reverse('notes-list') 
        response = client.post(url,data=note_data,content_type='application/json')
        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_note_invalid_data(self,client,generate_usertoken):
        note_data = {
            "title": "Test Note",
            "description": "This is a test note.",
            "color": "blue",
            "is_archive": "not_a_boolean", 
            "is_trash": False,
            "reminder": "invalid_date_format" 
        }
        url = reverse('notes-list') 
        response = client.post(
            url,
            data=note_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}'
        )
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_note_missing_fields(self,client,generate_usertoken):
        note_data = {
            "title": "",
            "description": "This is a test note.",
            "color": "blue",
            "is_archive": False,
            "is_trash": False,
            "reminder": "2024-08-29T12:00:00Z"
        }
        url = reverse('notes-list') 
        response = client.post(
            url,
            data=note_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}'
        )
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

#-------------------------get Notes------------------------------------------------------------
    

    def test_get_all_notes(self,client,generate_usertoken):
        url = reverse('notes-list')
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',content_type='application/json')
        # response_data=response.json()
        # print(f"response_data:{response_data['data']}")
        assert response.status_code == status.HTTP_200_OK

    def test_get_all_notes_unauthorized(self,client):
        url = reverse('notes-list')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_all_notes_invalid_token(self, client):
        url = reverse('notes-list')
        invalid_token = 'invalidtoken'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {invalid_token}', content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED



#-------------------------Update Note------------------------------------------------------------
    def test_update_note(self,client,generate_usertoken):
        
        note_id = self.test_note_create(client,generate_usertoken)
        data = {
            "title": "Meeting",
            "description": "Updated description",
            "reminder": "2024-08-26T11:50"
        }
        url = reverse('notes-detail', args=[note_id])
        response = client.put(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        
        assert response.status_code == status.HTTP_200_OK

    def test_update_note_unauthorized(self, client,generate_usertoken):
        note_id = self.test_note_create(client,generate_usertoken)
        data = {
            "title": "Updated Meeting",
            "description": "Updated description",
            "reminder": "2024-08-26T11:50"
        }
        url = reverse('notes-detail', args=[note_id])
        response = client.put(url, data=data, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_note_invalid_data(self, client, generate_usertoken):
        note_id = self.test_note_create(client, generate_usertoken)
        data = {
            "title": "Updated Meeting",
            "description": "Updated description",
            "reminder": "invalid_date_format" 
        }
        url = reverse('notes-detail', args=[note_id])
        response = client.put(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_non_existing_note(self, client, generate_usertoken):
        non_existing_note_id = 9999
        data = {
            "title": "Updated Meeting",
            "description": "Updated description",
            "reminder": "2024-08-26T11:50"
        }
        url = reverse('notes-detail', args=[non_existing_note_id])
        response = client.put(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_parital_update_note(self,client,generate_usertoken):
        note_id = self.test_note_create(client,generate_usertoken)
        data = {
        "title": "Meeting",
        "description": "Updated description",
        "is_trash": True,
        "reminder": "2024-08-26T11:50"
        }
        url = reverse('notes-detail', args=[note_id])
        response = client.patch(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK


#---------------------------------------------delete Note---------------------------------------------------
    def test_destory_note(self,client,generate_usertoken):
        note_id = self.test_note_create(client,generate_usertoken)
        url = reverse('notes-detail', args=[note_id])
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_destroy_note_unauthenticated(self, client,generate_usertoken):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-detail', args=[note_id])
        response = client.delete(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_destroy_note_invalid_id(self, client, generate_usertoken):
        invalid_note_id = 9999
        url = reverse('notes-detail', args=[invalid_note_id])
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_destroy_note_different_user(self, client, generate_usertoken, generate_usertoken2):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-detail', args=[note_id])
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}', content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST



#---------------------------------------------toggle archive Note---------------------------------------------------


    def test_toggle_archive_note_success(self, client, generate_usertoken):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-toggle-archive', args=[note_id])
        response = client.patch(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_toggle_archive_note_unauthenticated(self, client,generate_usertoken):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-toggle-archive', args=[note_id])
        response = client.patch(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_toggle_archive_note_invalid_id(self, client, generate_usertoken):
        invalid_note_id = 9999
        url = reverse('notes-toggle-archive', args=[invalid_note_id])
        response = client.patch(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_toggle_archive_note_different_user(self, client, generate_usertoken, generate_usertoken2):

        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-toggle-archive', args=[note_id])
        response = client.patch(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

#---------------------------------------------toggle trash Note---------------------------------------------------


    def test_toggle_trash_note_success(self, client, generate_usertoken):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-toggle-trash', args=[note_id])
        
        response = client.patch(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK

    def test_toggle_trash_note_unauthenticated(self, client,generate_usertoken):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-toggle-trash', args=[note_id])
        response = client.patch(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_trash_note_invalid_id(self, client, generate_usertoken):
        invalid_note_id = 9999
        url = reverse('notes-toggle-trash', args=[invalid_note_id])
        response = client.patch(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_toggle_trash_note_different_user(self, client, generate_usertoken, generate_usertoken2):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-toggle-trash', args=[note_id])
        response = client.patch(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

#---------------------------------------------get archieved Note---------------------------------------------------





    def test_get_archieved_notes(self, client, generate_usertoken):
        url = reverse('notes-archived-notes')
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_get_archived_notes_unauthenticated(self, client):
        url = reverse('notes-archived-notes')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_archived_notes_no_archived_notes(self, client, generate_usertoken):
        url = reverse('notes-archived-notes')
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        # assert response.json()['data'] == [] 

    def test_get_archived_notes_invalid_token(self, client):
        invalid_token = 'invalid_token'
        url = reverse('notes-archived-notes')
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {invalid_token}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


#---------------------------------------------get trashed Note---------------------------------------------------

    def test_get_trashed_notes(self, client, generate_usertoken):
        url = reverse('notes-trashed-notes')
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_get_trashed_notes_unauthenticated(self, client):
        url = reverse('notes-trashed-notes')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_trashed_notes_invalid_token(self, client):
        invalid_token = 'invalid_token'
        url = reverse('notes-trashed-notes')
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {invalid_token}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


#---------------------------------------------retrieve Note by id---------------------------------------------------

    def test_retrieve_note_success(self, client, generate_usertoken):
        """
        Test retrieving a specific note by ID from the cache.
        """
        note_id = self.test_note_create(client, generate_usertoken)

        url = reverse('notes-detail', args=[note_id])
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == note_id
        print("Retrieve note success response:", response.data)

    def test_retrieve_note_not_found(self, client, generate_usertoken):
        """
        Test retrieving a note that doesn't exist.
        """
        invalid_note_id = 9999 
        
        url = reverse('notes-detail', args=[invalid_note_id])
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_note_unauthenticated(self, client):
        note_id = 1
        url = reverse('notes-detail', args=[note_id])
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_note_different_user(self, client, generate_usertoken, generate_usertoken2):
        note_id = self.test_note_create(client, generate_usertoken)
        url = reverse('notes-detail', args=[note_id])
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
@pytest.mark.addLabel
class TestCollab:
    def test_note_create(self,client,generate_usertoken):
        data = {
            "title": "Meeting",
            "description": "This is the description of my secret note.",
            "color": "violet",
            "is_archive": True,
            "is_trash": False,
            "reminder":"2024-08-26T11:50"
        }
        url = reverse('notes-list')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',data=data,content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print("NOTE ID from user1=",response.data["data"]["id"])
        return response.data["data"]["id"]

    def test_note_create_by_2user(self,client,generate_usertoken2):
        
        data = {
            "title": "Meeting",
            "description": "This is the description of my secret note.",
            "color": "violet",
            "is_archive": True,
            "is_trash": False,
            "reminder":"2024-08-26T11:50"
        }
        url = reverse('notes-list')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',data=data,content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print(f"resonse data from user2= {response.data['data']} with use {response.data['data']['user']}")  
        return response.data['data']['user']

    def test_collab_add(self, client, generate_usertoken, generate_usertoken2):
        note_id = self.test_note_create(client, generate_usertoken)
        user_id = self.test_note_create_by_2user(client, generate_usertoken2)
        data = {
            "note_id": note_id,
            "user_id": [user_id],  
            "access_type": "read_write"
        }
        url = reverse('collaborators-add-collaborators')
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_collab_remove(self, client, generate_usertoken, generate_usertoken2):
        note_id = self.test_note_create(client, generate_usertoken)
        user_id = self.test_note_create_by_2user(client, generate_usertoken2)
        data = {
            "note_id": note_id,
            "user_id": [user_id], 
        }
        url = reverse('collaborators-remove-collaborators')
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@pytest.mark.coll
class TestLabels:

    def test_note_create(self,client,generate_usertoken):
        data = {
            "title": "Meeting",
            "description": "This is the description of my secret note.",
            "color": "violet",
            "is_archive": True,
            "is_trash": False,
            "reminder":"2024-08-26T11:50"
        }
        url = reverse('notes-list')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',data=data,content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print("NOTE ID=",response.data["data"]["id"])
        return response.data["data"]["id"]
    

    def test_label_create(self,client,generate_usertoken):
        data = {
            "name":"Cr7",
            "color":"Yellow"
        }
        url = reverse('label-list-create')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',data=data,content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print("LABEL ID=",response.data["id"])
        return response.data["id"]

    def test_add_labels_success(self, client, generate_usertoken):
        """
        Test case to successfully add labels to a note.
        """
        note_id = self.test_note_create(client, generate_usertoken)  
        label_id = self.test_label_create(client, generate_usertoken)  
        
        url = reverse('note-label-add-labels') 
        data = {
            "note_id": note_id,
            "label_ids": [label_id]
        }
        response = client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert "Labels added successfully" in response.data["message"]  
        print("Success response:", response.data)

    def test_add_labels_note_not_found(self, client, generate_usertoken):
        """
        Test case for adding labels to a note that does not exist.
        """
        url = reverse('note-label-add-labels')
        data = {
            "note_id": 9999, 
            "label_ids": [1]
        }
        response = client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Note not found" in response.data["error"] 
        print("Error response:", response.data)

    def test_add_labels_not_owner(self, client, generate_usertoken,generate_usertoken2):
        """
        Test case for adding labels to a note where the user is not the owner of the note.
        """
        note_id = self.test_note_create(client, generate_usertoken2)  

        label_id = self.test_label_create(client, generate_usertoken2)  
        
        url = reverse('note-label-add-labels')
        data = {
            "note_id": note_id,
            "label_ids": [label_id]
        }
        response = client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You are not the owner of this note." in response.data["error"] 
        print("Error response:", response.data)

    def test_add_labels_no_valid_labels(self, client, generate_usertoken):
        """
        Test case for adding labels where no valid labels are provided.
        """
        note_id = self.test_note_create(client, generate_usertoken) 
        
        url = reverse('note-label-add-labels')
        data = {
            "note_id": note_id,
            "label_ids": [9999] 
        }
        response = client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def create_note_and_label(self, client, generate_usertoken):
        """
        Utility function to create a note and a label, then return their IDs.
        """
        note_data = {
            "title": "Meeting",
            "description": "This is the description of my secret note.",
            "color": "violet",
            "is_archive": True,
            "is_trash": False,
            "reminder": "2024-08-26T11:50"
        }
        note_url = reverse('notes-list')
        note_response = client.post(note_url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=note_data, content_type='application/json')
        assert note_response.status_code == status.HTTP_201_CREATED
        note_id = note_response.data["data"]["id"]

        label_data = {
            "name": "Cr7",
            "color": "Yellow"
        }
        label_url = reverse('label-list-create')
        label_response = client.post(label_url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=label_data, content_type='application/json')
        assert label_response.status_code == status.HTTP_201_CREATED
        label_id = label_response.data["id"]

        return note_id, label_id

    def add_label_to_note(self, client, generate_usertoken, note_id, label_id):
        """
        Utility function to add a label to a note.
        """
        add_url = reverse('note-label-add-labels')
        add_data = {
            "note_id": note_id,
            "label_ids": [label_id]
        }
        add_response = client.post(add_url, data=add_data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert add_response.status_code == status.HTTP_200_OK
        assert "Labels added successfully" in add_response.data["message"]
        print("Label added to note:", add_response.data)

    def test_add_labels_success(self, client, generate_usertoken):
        """
        Test case to successfully add labels to a note.
        """
        note_id, label_id = self.create_note_and_label(client, generate_usertoken)
        self.add_label_to_note(client, generate_usertoken, note_id, label_id)

    def test_remove_labels_success(self, client, generate_usertoken):
        """
        Test case to successfully remove labels from a note.
        """
        note_id, label_id = self.create_note_and_label(client, generate_usertoken)

        self.add_label_to_note(client, generate_usertoken, note_id, label_id)

        remove_url = reverse('note-label-remove-labels')
        remove_data = {
            "note_id": note_id,
            "label_ids": [label_id]
        }
        remove_response = client.post(remove_url, data=remove_data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert remove_response.status_code == status.HTTP_200_OK
        assert "Labels removed successfully" in remove_response.data["message"]
        print("Label removed from note:", remove_response.data)


    def test_remove_labels_not_owner(self, client, generate_usertoken, generate_usertoken2):
        """
        Test case to ensure a user cannot remove labels from a note they don't own.
        """
        note_id, label_id = self.create_note_and_label(client, generate_usertoken2) 

        remove_url = reverse('note-label-remove-labels')
        remove_data = {
            "note_id": note_id,
            "label_ids": [label_id]
        }
        remove_response = client.post(remove_url, data=remove_data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert remove_response.status_code == status.HTTP_403_FORBIDDEN
        assert "You are not the owner of this note." in remove_response.data["error"]

    def test_remove_non_existent_label(self, client, generate_usertoken):
        """
        Test case for attempting to remove a non-existent label from a note.
        """
        note_id, label_id = self.create_note_and_label(client, generate_usertoken)

        self.add_label_to_note(client, generate_usertoken, note_id, label_id)

        non_existent_label_id = label_id + 1 
        remove_url = reverse('note-label-remove-labels')
        remove_data = {
            "note_id": note_id,
            "label_ids": [non_existent_label_id]
        }
        remove_response = client.post(remove_url, data=remove_data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert remove_response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_remove_labels_not_assigned(self, client, generate_usertoken):
        """
        Test case for attempting to remove a label that isn't assigned to the note.
        """
        note_id, label_id = self.create_note_and_label(client, generate_usertoken)

        remove_url = reverse('note-label-remove-labels')
        remove_data = {
            "note_id": note_id,
            "label_ids": [label_id]
        }
        remove_response = client.post(remove_url, data=remove_data, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert remove_response.status_code == status.HTTP_400_BAD_REQUEST
    


    

    






