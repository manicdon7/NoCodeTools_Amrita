from django.shortcuts import render
from web3 import Web3


def index(request):
    # Connect to the local Ethereum node
    web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

    # Get the first account from the connected wallet
    account = web3.eth.accounts[0]

    # Render the web page with the account address
    return render(request, 'index.html', {'account': account})
