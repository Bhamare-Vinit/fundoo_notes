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
@pytest.mark.label
class TestLabels:

#-------------------------Create Label--------------------------------------------------------------
    def test_label_create(self,client,generate_usertoken):
        data = {
            "name":"Cr7",
            "color":"Yellow"
        }
        url = reverse('label-list-create')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',data=data,content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print("response",response.data["id"])
        return response.data["id"]
    
    def test_label_create_missing_name(self, client, generate_usertoken):
        data = {
            "color": "Yellow"
        }
        url = reverse('label-list-create')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_label_create_number_data(self, client, generate_usertoken):
        data = {
            "name": 123,
            "color": "Yellow"
        }
        url = reverse('label-list-create')
        response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_label_create_unautho(self, client):
        data = {
            "name": "Cr7",
            "color": "Yellow"
        }
        url = reverse('label-list-create')
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

#-------------------------get Notes------------------------------------------------------------
    

    def test_get_all_labels(self,client,generate_usertoken):
        url = reverse('label-list-create')
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}',content_type='application/json')
        response_data=response.json()
        print(f"response_data:{response_data}")
        assert response.status_code == status.HTTP_200_OK

    def test_get_all_labels_unautho(self, client):
        url = reverse('label-list-create')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    

    #---------------------------------------------retrieve Note by id---------------------------------------------------

    def test_retrieve_label_success(self, client, generate_usertoken):
        """
        Test retrieving a specific note by ID from the cache.
        """
        label_id = self.test_label_create(client, generate_usertoken)

        url = reverse('label-detail', args=[label_id])
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        print("Response:", response.data)
        assert response.data['id'] == label_id
        print("Retrieve note success response:", response.data)

    def test_retrieve_label_not_found(self, client, generate_usertoken):
        label_id = 999
        url = reverse('label-detail', args=[label_id])
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        # print("Response:", response.data)
        # assert response.data['id'] == label_id
        # print("Retrieve note success response:", response.data)


    def test_retrieve_label_different_user(self, client, generate_usertoken, generate_usertoken2):
        label_id = self.test_label_create(client, generate_usertoken)
        
        url = reverse('label-detail', args=[label_id])
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',
            content_type='application/json'
        )
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


#-------------------------Update Note------------------------------------------------------------
    def test_update_label(self,client,generate_usertoken):
        
        note_id = self.test_label_create(client,generate_usertoken)
        data = {
            "name":"Cr7777777777",
            "color":"Yellow"
        }
        url = reverse('label-detail', args=[note_id])
        response = client.put(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_update_label_invalid_data(self, client, generate_usertoken):
        label_id = self.test_label_create(client, generate_usertoken)
        data = {
            "name": "",
            "color": "Yellow"
        }
        url = reverse('label-detail', args=[label_id])
        response = client.put(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_label_not_found(self, client, generate_usertoken):
        invalid_label_id = 9999
        data = {
            "name": "Cr7777777777",
            "color": "Yellow"
        }
        url = reverse('label-detail', args=[invalid_label_id])
        response = client.put(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', data=data, content_type='application/json')

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        # print("Update label not found response:", response.data)

    def test_update_label_unauthenticated(self, client):
        """
        Test updating a label without being authenticated.
        """
        label_id = 1 
        data = {
            "name": "Cr7777777777",
            "color": "Yellow"
        }
        url = reverse('label-detail', args=[label_id])
        response = client.put(url, data=data, content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        print("Update label unauthenticated response:", response.data)

    def test_update_label_different_user(self, client, generate_usertoken, generate_usertoken2):
        """
        Test updating a label created by one user using a different user's token.
        """
        label_id = self.test_label_create(client, generate_usertoken)
        data = {
            "name": "Cr7777777777",
            "color": "Yellow"
        }
        url = reverse('label-detail', args=[label_id])
        response = client.put(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',
            data=data,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        print("Update label different user response:", response.data)
    

#---------------------------------------------delete Note---------------------------------------------------
    def test_destory_label(self,client,generate_usertoken):
        note_id = self.test_label_create(client,generate_usertoken)
        url = reverse('label-detail', args=[note_id])
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    
    def test_destroy_label_not_found(self, client, generate_usertoken):
        invalid_label_id = 9999
        url = reverse('label-detail', args=[invalid_label_id])
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {generate_usertoken}', content_type='application/json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        print("Destroy label not found response:", response.data)

    def test_destroy_label_unauthenticated(self, client):
        """
        Test deleting a label without being authenticated.
        """
        label_id = 1 
        url = reverse('label-detail', args=[label_id])
        response = client.delete(url, content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        print("Destroy label unauthenticated response:", response.data)

    def test_destroy_label_different_user(self, client,generate_usertoken, generate_usertoken2):
        """
        Test deleting a label created by one user using a different user's token.
        """
        label_id = self.test_label_create(client, generate_usertoken)
        print(f"label_id: {label_id}")
        url = reverse('label-detail', args=[label_id])
        response = client.delete(
            url,
            HTTP_AUTHORIZATION=f'Bearer {generate_usertoken2}',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        #it is giving 404 because i used queryset to get labels owned by user
        #then find label_Id in that queryset and delete it
        #but  that label is not in that user's label hence showing not found 404

        
    


    

