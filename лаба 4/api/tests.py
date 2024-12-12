from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from currency.models import Currency
from .serializers import CurrencySerializer

# Create your tests here.
class AuthTests(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_token_obtain_pair(self):
        url = reverse('api:token_obtain_pair')
        response = self.client.post(url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        url = reverse('api:token_obtain_pair')
        response = self.client.post(url, {'username': self.username, 'password': self.password})
        refresh_token = response.data['refresh']

        url_refresh = reverse('api:token_refresh')
        response = self.client.post(url_refresh, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_verify(self):
        url = reverse('api:token_obtain_pair')
        response = self.client.post(url, {'username': self.username, 'password': self.password})
        access_token = response.data['access']

        url_verify = reverse('api:token_verify')
        response = self.client.post(url_verify, {'token': access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CurrencyExchangeTests(APITestCase):

    def setUp(self):
        self.test1 = Currency.objects.create(
            UID='ts1',
            NumCode='ts1',
            CharCode='ts1',
            Nominal=1,
            Name='Test1',
            Value=1.0,
            Previous=1.0
        )
        
        self.test2 = Currency.objects.create(
            UID='ts2',
            NumCode='ts2',
            CharCode='ts2',
            Nominal=1,
            Name='Test2',
            Value=0.85,
            Previous=0.80
        )
        
        self.test1.save()
        self.test2.save()

    def authenticate_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        url = reverse('api:token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        return response.data['access']

    def test_currency_exchange_get(self):
        access_token = self.authenticate_user()
        
        url = reverse('api:currency_exchange')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_currency_exchange_post_valid_data(self):
        access_token = self.authenticate_user()
        
        url = reverse('api:currency_exchange')
        
        data = {
            'currencyFrom': 'ts1',
            'currencyTo': 'ts2',
            'ammount': 100
        }
        
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(self.test1.exchange_to(data['ammount'], self.test2)), response.data)  # Убедитесь, что ответ содержит информацию о валюте

    def test_currency_exchange_invalid_From_data(self):
        access_token = self.authenticate_user()
        
        url = reverse('api:currency_exchange')
        
        data = {
            'currencyFrom': 'INVALID',
            'currencyTo': 'ts2',
            'ammount': 100
        }
        
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_currency_exchange_invalid_To_data(self):
        access_token = self.authenticate_user()
        
        url = reverse('api:currency_exchange')
        
        data = {
            'currencyFrom': 'ts1',
            'currencyTo': 'INVALID',
            'ammount': 100
        }
        
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_currency_exchange_invalid_ammount_data(self):
        access_token = self.authenticate_user()
        
        url = reverse('api:currency_exchange')
        
        data = {
            'currencyFrom': 'ts1',
            'currencyTo': 'ts2',
            'ammount': 'Invalid'
        }
        
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)