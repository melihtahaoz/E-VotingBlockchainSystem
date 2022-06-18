from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.contrib import messages
from .forms import VoterSignUpForm
from .models import Candidate, Voter

def index(request):
    return render(request, 'home.html')

def loginPage(request):
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return render(request, 'home.html')

def voter_main(request):
    candidate_list = Candidate.objects.all()
    return render(request, 'voter_main.html', {'candidate_list': candidate_list})

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
    return render(request, 'registration/login.html',context={'form':AuthenticationForm()})

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

class voter_register(CreateView):
    model = Voter  
    form_class = VoterSignUpForm
    template_name= 'voter_register.html'
    def form_valid(self, form):
        voter = form.save()
        new_voter = Voter()
        new_voter.u_name = form.cleaned_data.get('username')
        new_voter.mail_addr = form.cleaned_data.get('mail_addr')
        new_voter.save()

        login(self.request, voter)
        return redirect('/voter_main')

