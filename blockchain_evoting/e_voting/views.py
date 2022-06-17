from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages

def index(request):
    return render(request, 'home.html')

def loginPage(request):
    return render(request, 'login.html')

def login_voter(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/login')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'home.html',context={'form':AuthenticationForm()})

def login_admin(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/admin')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'home.html',context={'form':AuthenticationForm()})
