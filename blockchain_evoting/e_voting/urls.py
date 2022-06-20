from django.urls import path
from . import views

app_name = "e_voting"
urlpatterns = [
    path('',views.index, name='index'),
    path('admin/', views.login_admin, name='login_admin'),
    path('login', views.login_voter, name='login_voter'),
    path('log_out', views.log_out, name='log_out'),
    #path('loginPage/', views.loginPage, name='loginPage'),
    path('voter_register/', views.voter_register.as_view(), name='voter_register'),
    path('voter_main', views.voter_main, name='voter_main'),
    path('accounts/profile/', views.voter_main, name='voter_main'),
    path('vote/<str:name>', views.vote, name='vote'),
    ]