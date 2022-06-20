from django.urls import path
from . import views

app_name = "e_voting"
urlpatterns = [
    path('',views.index, name='index'),
    path('adminege/', views.login_admin, name='login_admin'),
    path('login', views.login_voter, name='login_voter'),
    path('log_out', views.log_out, name='log_out'),
    #path('loginPage/', views.loginPage, name='loginPage'),
    path('voter_register/', views.voter_register.as_view(), name='voter_register'),
    path('voter_main', views.voter_main, name='voter_main'),
    path('accounts/profile/', views.voter_main, name='voter_main'),
    path('vote/<str:name>', views.vote, name='vote'),
    path('add_candidate', views.add_candidate, name='add_candidate'),
    path('next_state_add_voter', views.next_state_add_voter, name='next_state_add_voter'),
    path('add_voter', views.add_voter, name='add_voter'),
    ]