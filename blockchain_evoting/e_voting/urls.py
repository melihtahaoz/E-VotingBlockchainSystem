from django.urls import path
from .views import index

app_name = "e_voting"
urlpatterns = [
    path('',index, name='index'),
]