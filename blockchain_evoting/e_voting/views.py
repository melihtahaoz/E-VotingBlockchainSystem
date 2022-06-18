from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.contrib import messages
from .forms import VoterSignUpForm
from .models import Candidate, Voter, Vote

def index(request):
    return render(request, 'home.html')

def loginPage(request):
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return render(request, 'home.html')

def voter_main(request,):
    print(request.user)
    voter = Voter.objects.filter(u_name=request.user.username)[0]
    if(voter.eligibility):
        candidate_list = Candidate.objects.all()
        return render(request, 'voter_main.html', {'candidate_list': candidate_list})
    else:
        #TO DO: integrate you are not eligible! message to the voter_main page here
        return HttpResponse("yoooooooo")

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

def vote(request,name):
    print(request.user)
    voter = Voter.objects.filter(u_name=request.user.username)[0]
    candidate = Candidate.objects.filter(name=name)[0]
    if request.method == 'POST' and request.user.is_authenticated and not voter.has_voted:
        new_vote = Vote(candidate=candidate,voter=voter)
        new_vote.save()
        voter.has_voted = 1
        voter.save(update_fields=['has_voted'])
        candidate.vote_count += 1
        candidate.save(update_fields=['vote_count'])
        #TO DO: after voting, show a different page that says you have voted and the evidence etc. - maybe after integrating blockchain
        response = redirect('/voter_main')
        return response 
    else:
        #TO DO: integrate you already voted! message to the voter_main page here
        return HttpResponse("user has already voted!\n\n")

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

