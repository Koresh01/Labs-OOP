from django.contrib import admin
from django.urls import path
from dictApp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('home/',home,name="home"),
    path('words_list/',words_list,name="words_list"),
    path('add_word/',add_word,name="add_word"),
    
]
