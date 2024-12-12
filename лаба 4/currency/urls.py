from django.urls import path
from . import views
# from .views import get_exchange_rate
app_name = 'currency'

urlpatterns = [
    path('currency/exchange/', views.index, name='index'),
    
    path('auth/login/', views.UserLogin, name='login'),
    path('auth/register/', views.UserRegister, name='register'),
    path('auth/logout/', views.UserLogout, name='logout'),
]