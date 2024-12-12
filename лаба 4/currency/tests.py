from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Currency
class AuthTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_valid_user(self):
        response = self.client.post(reverse('currency:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_user(self):
        response = self.client.post(reverse('currency:login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid Username or Password')

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('currency:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_new_user(self):
        response = self.client.post(reverse('currency:register'), {
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newuser')
        self.assertIsNotNone(new_user)
        
class CurrencyTests(TestCase):
    
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
    
    def test_exchange(self):
        self.ammount = 100
        exchanged_ammount = self.test1.exchange_to(self.ammount, self.test2)
        
        self.assertEqual(exchanged_ammount, self.ammount * (self.test1.Value / self.test1.Nominal) * (self.test2.Nominal / self.test2.Value))
