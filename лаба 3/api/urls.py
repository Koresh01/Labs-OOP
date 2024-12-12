from django.urls import path
from api.views import get_token,get_goods,new_good


app_name = 'api'

urlpatterns = [
    path('get_token/', get_token, name='get_token'),
    path('get_goods/',get_goods,name='get_goods'),
    path('new_good/',new_good,name='new_good')
]