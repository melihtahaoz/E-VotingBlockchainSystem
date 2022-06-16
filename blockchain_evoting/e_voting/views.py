from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.admin.forms import AuthenticationForm

def index(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('index')
    else:  
        form = AuthenticationForm()
    return render(request, 'login.html')