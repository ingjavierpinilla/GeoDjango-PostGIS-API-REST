from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from api.models import Dataset, Row

class TestViews(TestCase):

    def setUp(self):

        #Autenticacion de usuario
        self.user = User.objects.create_user(username='tester', email='', password='pass_magentrack')
        self.client = APIClient()
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

        #reverse de las diferentes url
        self.dataset_list_create_url = reverse('dataset-list-create')
        self.row_list_url = reverse('row-list')
        self.log_list_url = reverse('log-list')
        self.log_list_site_url = reverse('log-list-site')
    
    def test_dataset_list_create_url_GET(self):

        response = self.client.get(self.dataset_list_create_url)

        #verificacion de status_code 200 
        self.assertEquals(response.status_code, 200)

        #verificacion de tipo de respuesta, JSON
        self.assertIsInstance(response.data, dict) 
        #verificacion de tipo de status_code 401 cuando se quitan las credenciales
        self.client.credentials()
        response = self.client.get(self.dataset_list_create_url)
        self.assertEquals(response.status_code, 401)

    def test_log_list_url_GET(self):

        response = self.client.get(self.log_list_url)

        #verificacion de status_code 200 
        self.assertEquals(response.status_code, 200)

        #verificacion de tipo de respuesta, lista (no hice uso de serializer)
        self.assertIsInstance(response.data, (list, dict)) 
        
        #verificacion de tipo de status_code 401 cuando se quitan las credenciales
        self.client.credentials()
        response = self.client.get(self.log_list_url)
        self.assertEquals(response.status_code, 401)
    
    def test_log_list_site_url_GET(self):

        response = self.client.get(self.log_list_site_url)

        #verificacion de status_code 200
        self.assertEquals(response.status_code, 200)

        #verificacion del template usado para presentar los logs
        self.assertTemplateUsed(response, 'log/log_table.html')
    
    def test_row_list_url_GET(self):
        
        #verificacion de status_code 400, bad request, falta dataset_id
        response = self.client.get(self.row_list_url)
        self.assertEquals(response.status_code, 400, 'falta dataset_id')

        #verificacion de status_code 400, bad request, dataset_id vacio
        response = self.client.get(self.row_list_url, {'dataset_id': ''})
        self.assertEquals(response.status_code, 400, 'dataset_id vacio')

        #verificacion de status_code 400, bad request, dataset_id no int
        response = self.client.get(self.row_list_url, {'dataset_id': 'test'})
        self.assertEquals(response.status_code, 400, 'dataset_id no int')

        #verificacion de status_code 400, bad request, dataset_id no int, blank
        response = self.client.get(self.row_list_url, {'dataset_id': '  '})
        self.assertEquals(response.status_code, 400, 'dataset_id no int. blank')

        #verificacion de status_code 200, dataset_id valido
        response = self.client.get(self.row_list_url, {'dataset_id': '1'})
        self.assertEquals(response.status_code, 200, 'dataset_id valido')

        #verificacion de status_code 200, punto valido
        response = self.client.get(self.row_list_url, {'dataset_id': '1', 'punto': '(1,11)'})
        self.assertEquals(response.status_code, 200, 'punto valido')

        #verificacion de status_code 200; dataset_id, punto y name validos
        response = self.client.get(self.row_list_url, {'dataset_id': '1', 'punto': '1,11', 'name': 'ram'})
        self.assertEquals(response.status_code, 200, 'dataset_id, punto y name validos')
        #verificacion de tipo de respuesta, JSON
        self.assertIsInstance(response.data, (list, dict)) 
