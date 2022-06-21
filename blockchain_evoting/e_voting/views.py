import operator
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.contrib import messages
from .forms import VoterSignUpForm
from .models import Candidate, Voter
from web3 import Web3
import solcx
from solcx import compile_standard
import json
voting_started = False
voting_finished = False
election_instance = None
solcx.install_solc('0.7.0')

with open(r"C:\Users\Batuhan Demir\Desktop\repos\E-VotingBlockchainSystem\blockchain_evoting\e_voting\Election.sol", "r") as file:
 election_file = file.read()


compiled_sol = compile_standard(
  { 
    "language": "Solidity",
    "sources": {"Election.sol": {"content": election_file}},
    "settings": {
      "outputSelection": {
        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
      }
    },
  },
  solc_version = "0.7.0",
)

with open("compiled_code.json", "w") as file:
  json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["Election.sol"]["Election"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["Election.sol"]["Election"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337

admin_address = "0xfe3bEba413D7E9F10Bdb91E2CA36cA199ef57BA0"
admin_private = "0xf6e2ec54c7bb046eeb01a7e6c34c614a00f231178a974869caab57793eec4d8d"

Election = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(admin_address)
print(nonce)

# Submit the transaction that deploys the contract
def deploy_election(Election, nonce, name):
  transaction = Election.constructor(name).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": admin_address,
        "nonce": nonce,
    }
  )
  nonce += 1
  # Sign the transaction
  signed_txn = w3.eth.account.sign_transaction(transaction, private_key=admin_private)
  print("Deploying Contract!")
  # Send it!
  tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  # Wait for the transaction to be mined, and get the transaction receipt
  print("Waiting for transaction to finish...")
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print(f"Done! Contract deployed to {tx_receipt.contractAddress}") 

  election_instance = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
  return election_instance, nonce

def addCandidate(election_instance, nonce, candidate_name):
	store_transaction = election_instance.functions.addCandidate(candidate_name).buildTransaction(
			{
				"chainId": chain_id,
				"gasPrice": w3.eth.gas_price,
				"from": admin_address,
				"nonce": nonce,
		}
	)
	nonce += 1

	signed_greeting_txn = w3.eth.account.sign_transaction(
		store_transaction, private_key=admin_private
	)

	tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
	print("Updating stored Value...")
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
	return nonce

def addVoter(election_instance, nonce, voter_username, voter_address):
	store_transaction = election_instance.functions.AddVoter(voter_username, voter_address).buildTransaction(
			{
				"chainId": chain_id,
				"gasPrice": w3.eth.gas_price,
				"from": admin_address,
				"nonce": nonce,
		}
	)
	nonce += 1

	signed_greeting_txn = w3.eth.account.sign_transaction(
		store_transaction, private_key=admin_private
	)

	tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
	print("Updating stored Value...")
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
	return nonce


def nextStateAddVoter(election_instance, nonce):
	store_transaction = election_instance.functions.nextStateAddVoter().buildTransaction(
			{
				"chainId": chain_id,
				"gasPrice": w3.eth.gas_price,
				"from": admin_address,
				"nonce": nonce,
		}
	)
	nonce += 1

	signed_greeting_txn = w3.eth.account.sign_transaction(
		store_transaction, private_key=admin_private
	)

	tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
	print("Updating stored Value...")
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
	return nonce

def nextStateVoting(election_instance, nonce):
	store_transaction = election_instance.functions.nextStateVoting().buildTransaction(
			{
				"chainId": chain_id,
				"gasPrice": w3.eth.gas_price,
				"from": admin_address,
				"nonce": nonce,
		}
	)
	nonce += 1

	signed_greeting_txn = w3.eth.account.sign_transaction(
		store_transaction, private_key=admin_private
	)

	tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
	print("Updating stored Value...")
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
	return nonce

def nextStateFinishing(election_instance, nonce):
	store_transaction = election_instance.functions.nextStateFinishing().buildTransaction(
			{
				"chainId": chain_id,
				"gasPrice": w3.eth.gas_price,
				"from": admin_address,
				"nonce": nonce,
		}
	)
	nonce += 1

	signed_greeting_txn = w3.eth.account.sign_transaction(
		store_transaction, private_key=admin_private
	)

	tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
	print("Updating stored Value...")
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
	return nonce

def voting(election_instance, nonce, candidate_name, voter_public, voter_private):
	store_transaction = election_instance.functions.VotingProgressing(candidate_name).buildTransaction(
			{
				"chainId": chain_id,
				"gasPrice": w3.eth.gas_price,
				"from": voter_public,
				"nonce": nonce,
		}
	)
	
	signed_greeting_txn = w3.eth.account.sign_transaction(
		store_transaction, private_key=voter_private
	)

	tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
	print("Vote is being saved...")
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
	print(tx_receipt)
	
def isUserVoted(election_instance, voter_address):
	return election_instance.functions.isUserVoted(voter_address).call()

def getElectionName(election_instance):
  return election_instance.functions.getElectionName().call()

def getCandidateNames(election_instance):
  return election_instance.functions.getCandidateNames().call()

def getNumOfCandidates(election_instance):
  return election_instance.functions.getNumOfCandidates().call()

def getResultsValue(election_instance, candidate_name):
  return election_instance.functions.getResultsValue(candidate_name).call()


## ENDPOINTSS
def index(request):
    return render(request, 'home.html')

def loginPage(request):
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return render(request, 'home.html')

def voter_main(request):
	global election_instance
	global voting_started
	voter = Voter.objects.filter(u_name=request.user.username)[0]
	voted = isUserVoted(election_instance,'0x69531a9ec2E2CB27BD2dfe94C9d0A998C111c1e0')
	print("Voted:",voted)
	if voting_started:
		if(not voted):
			candidate_list = getCandidateNames(election_instance)
			return render(request, 'voter_main.html', {'candidate_list': candidate_list})
		else:
				#TO DO: integrate you are not eligible! message to the voter_main page here
			return HttpResponse("You already voted! Here is the receipt: ")
	else:
		return HttpResponse("Voting has not started yet! Try later!")

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

def welcome_admin(request):
	return render(request,'welcome_admin.html')

def login_admin(request):
    global nonce
    global election_instance
    print(nonce)
    election_instance, nonce2 = deploy_election(Election, nonce, "Election Test")
    nonce = nonce2
    print(nonce)
    return render(request, 'admin_main.html')

def vote(request,name):
	print(request.user)
	#voter = Voter.objects.filter(u_name=request.user.username)[0]
	#candidate = Candidate.objects.filter(name=name)[0]
	if request.method == 'POST' and request.user.is_authenticated:
		#voter.has_voted = 1
		#voter.save(update_fields=['has_voted'])
		#candidate.save(update_fields=['vote_count'])
		#TO DO: after voting, show a different page that says you have voted and the evidence etc. - maybe after integrating blockchain
		address = request.POST.get('Address')
		private_key = request.POST.get('private_key')
		print(address)
		global election_instance
		global admin_private
		voting(election_instance,0,name,address,private_key)
		response = redirect('/voter_main')
		return response 
	else:
	#TO DO: integrate you already voted! message to the voter_main page here
		return HttpResponse("user has already voted!\n\n")

class voter_register(CreateView):
    global nonce
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

def add_candidate(request):
    global nonce
    global election_instance
    if request.method=='POST':
        data = request.POST
        candidate_name = data["fname"]
        nonce2 = addCandidate(election_instance, nonce, candidate_name)
        nonce = nonce2
        print(nonce)
    return render(request, 'admin_main.html')

def next_state_add_voter(request):
    global nonce
    global election_instance
    nonce2 = nextStateAddVoter(election_instance, nonce)
    nonce = nonce2
    print(nonce)
    return redirect('/add_voter_panel')

def add_voter_panel(request):
	return render(request, 'add_voter_panel.html')

def add_voter(request):
    global nonce
    global election_instance
    if request.method== 'POST':
        data = request.POST
        votername = data["votername"]
        voteraddress = data["voteraddress"]
        nonce2 = addVoter(election_instance, nonce, votername, voteraddress)
        nonce = nonce2
        print(nonce)
    return render(request, 'add_voter_panel.html')

def voting_panel(request):
	return render(request,'voting_status.html',{'voting_finished': voting_finished,'voting_started': voting_started})

def next_state_voting(request):
	global voting_started
	global nonce
	global election_instance
	nonce2 = nextStateVoting(election_instance,nonce)
	voting_started = True
	print("Voting has started...")
	nonce = nonce2
	print(nonce)
	return render(request,'voting_status.html',{'voting_finished': voting_finished,'voting_started': voting_started})

def next_state_finish(request):
	global voting_finished
	global voting_started
	global nonce
	global election_instance
	nonce2 = nextStateFinishing(election_instance,nonce)
	voting_finished = True
	voting_started = False
	nonce = nonce2
	print(nonce)
	return render(request,'voting_status.html',{'voting_finished': voting_finished,'voting_started': voting_started})

def results(request):
	global election_instance
	candidates = getCandidateNames(election_instance)
	resultsMap = {}
	for candidate in candidates:
		resultsMap[candidate] = getResultsValue(election_instance,candidate)
	
	winner = max(results.items(), key=results.get)
	print(winner)
	return render(request,'results.html',{'results':resultsMap, 'candidates': candidates,'winner': winner})