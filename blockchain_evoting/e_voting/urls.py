from django.urls import path
from . import views

app_name = "e_voting"
urlpatterns = [
    path('',views.index, name='index'),
    path('admin/', views.login_admin, name='login_admin')
]