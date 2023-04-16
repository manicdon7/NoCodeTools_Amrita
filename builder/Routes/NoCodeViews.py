from bs4 import BeautifulSoup
import htmlmin
import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from ..models import Pages, ChatMessage, Blog
from django.core.serializers import serialize
import json
from .Tool.Tools import random_image
from .AI_Functions import Code_scriping
import io
from django.http import FileResponse
from .Auto_generate_html import Make_web
# Create your views here.
from web3 import Web3, HTTPProvider
from WebpageBuilderDjango.settings import my_address, private_key
import os
w3 = Web3(Web3.HTTPProvider(
    'https://polygon-mumbai.g.alchemy.com/v2/K59YdNGK95akCLJrA1m9nYPZ7JYNa8Me'))


def index(request):
    pages = Pages.objects.all()
    return render(request, 'NoCodeBuilderPages/pages.html', {"pages": pages})


def connect_metamask(request):
    # Connect to the local blockchain node
    web3 = Web3(HTTPProvider(
        'https://polygon-mumbai.g.alchemy.com/v2/K59YdNGK95akCLJrA1m9nYPZ7JYNa8Me'))
    return render(request, 'common/index.html')


def addPage(request):
    return render(request, 'NoCodeBuilderPages/index.html')


def savePage(request):
    if (request.method == 'POST'):
        html = request.POST['html']
        css = request.POST['css']
        Project_name = request.POST['Project_name']

        id = 1
        # Ploygon >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        name = Project_name
        image = random_image()
        description = 'Description of Page 1'
        html = html
        css = css
        preview_link = 'http://localhost:8000/page1/'

        # set the contract address and ABI
        contract_address = '0x6C9e539874f9aD5C4D277cEc5D8DF76349a5028B'
        contract_abi = json.loads('[ { "inputs": [ { "internalType": "uint256", "name": "id", "type": "uint256" }, { "internalType": "string", "name": "name", "type": "string" }, { "internalType": "string", "name": "image", "type": "string" }, { "internalType": "string", "name": "description", "type": "string" }, { "internalType": "string", "name": "html", "type": "string" }, { "internalType": "string", "name": "css", "type": "string" }, { "internalType": "string", "name": "previewLink", "type": "string" } ], "name": "addPage", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "id", "type": "uint256" } ], "name": "getPage", "outputs": [ { "internalType": "string", "name": "", "type": "string" }, { "internalType": "string", "name": "", "type": "string" }, { "internalType": "string", "name": "", "type": "string" }, { "internalType": "string", "name": "", "type": "string" }, { "internalType": "string", "name": "", "type": "string" }, { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "pages", "outputs": [ { "internalType": "string", "name": "name", "type": "string" }, { "internalType": "string", "name": "image", "type": "string" }, { "internalType": "string", "name": "description", "type": "string" }, { "internalType": "string", "name": "html", "type": "string" }, { "internalType": "string", "name": "css", "type": "string" }, { "internalType": "string", "name": "preview_link", "type": "string" } ], "stateMutability": "view", "type": "function" } ]')

        # create an instance of the contract
        simple_storage = w3.eth.contract(
            address=contract_address, abi=contract_abi)
        nonce = w3.eth.getTransactionCount(my_address)

        print("transaction sucess..")

        greeting_transaction = simple_storage.functions.addPage(
            id, name, image, description, html, css, preview_link).buildTransaction(
            {
                "chainId": w3.eth.chainId,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                # the initial nonce should "orginal nonce value" after that you should be increase nonce
                "nonce": nonce,
            }
        )

        # Wait for the transaction to be mined
        signed_txn = w3.eth.account.sign_transaction(
            greeting_transaction, private_key=private_key)

        # send the signed transaction to the network
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # get the transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print("Transaction hash code : ", tx_receipt,
              'Block number : ', tx_receipt.blockNumber)
        # ----------------------------------------------------------------------------------------------------------------------

        with open('_'.join(name.split())+'.html', 'w', encoding='utf-8') as fs:
            fs.write(html)
        fs.close()

        url = "https://api.verbwire.com/v1/nft/store/file"

        files = {"filePath": ('_'.join(name.split())+'.html', open(
            '_'.join(name.split())+'.html', "rb"), "text/html")}
        headers = {
            "accept": "application/json",
            "X-API-Key": "sk_live_fdd243a1-07c3-4c90-a976-c133c47f1b3a"
        }
        response_1 = requests.post(url, files=files, headers=headers)
        print(response_1.text)

        with open('_'.join(name.split())+'.css', 'w', encoding='utf-8') as fs:
            fs.write(css)
        fs.close()
        url = "https://api.verbwire.com/v1/nft/store/file"

        files = {"filePath": ('_'.join(name.split())+'.css', open(
            '_'.join(name.split())+'.css', "rb"), "text/css")}
        headers = {
            "accept": "application/json",
            "X-API-Key": "sk_live_fdd243a1-07c3-4c90-a976-c133c47f1b3a"
        }

        response_2 = requests.post(url, files=files, headers=headers)

        print(response_2.text)

        # ------------------------------------ html with css -----------------------------------------------------------------
        with open('_'.join(name.split())+'(1).html', 'w', encoding='utf-8') as fs:
            fs.write(html+f"""<style>{css}</style>""")
        fs.close()
        url = "https://api.verbwire.com/v1/nft/store/file"

        files = {"filePath": ('_'.join(name.split())+'.css', open(
            '_'.join(name.split())+'.css', "rb"), "text/css")}
        headers = {
            "accept": "application/json",
            "X-API-Key": "sk_live_fdd243a1-07c3-4c90-a976-c133c47f1b3a"
        }

        response_3 = requests.post(url, files=files, headers=headers)

        print(response_3.text)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End Polygone >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Data Base >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        page = Pages.objects.create(
            name=Project_name, html=html, css=css, image=random_image(), Block_chin_blockNo=tx_receipt.blockNumber, trans_detial=tx_receipt, ipfs=response_1.text+" "+response_2.text+" "+response_3.text)
        page.save()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>End DB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    return JsonResponse({"result": (json.loads(serialize('json', [page])))[0]})


def editPage(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'NoCodeBuilderPages/index.html', {"page": page})


def block_detials(request, block):
    data = Pages.objects.get(Block_chin_blockNo=block)
    return render(request, 'block.html', {'block_detials': data})


def blog_block_detials(request, block):
    data = Blog.objects.get(Block_chin_blockNo=block)
    return render(request, 'block.html', {'block_detials': data})


def editPageContent(request, id):
    if (request.method == 'POST'):
        html = request.POST['html']
        css = request.POST['css']
        page = Pages.objects.get(pk=id)
        page.html = html
        page.css = css
        page.save()
    return JsonResponse({"result": (json.loads(serialize('json', [page])))[0]})


def previewPage(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'NoCodeBuilderPages/preview.html', {"page": page})


def ResumeBuilder(request):

    return render(request, 'NoCodeBuilderPages/resume_maker.html')


def Own_Gpt(request):
    return render(request, 'gpt\index.html')


def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = Code_scriping(prompt)
        chat_message = ChatMessage(prompt=prompt, response=response)
        chat_message.save()
        return JsonResponse({'bot': response})

    return render(request, 'gpt/index.html', {'chat_messages': ChatMessage.objects.all()})


def autogenerate(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        ProjectName = request.POST.get('ProjectName')
        print(query, ProjectName)
        a = Make_web(query, ProjectName)
        print("connected..........")
        code = a.create_page()
        print("buffering.....")
        buffer = io.BytesIO()
        buffer.write(code.encode('utf-8'))
        buffer.seek(0)
        # Generate a file name for the minified HTML file
        filename = 'Generated_code.html'

        # Create a FileResponse object with the minified HTML data and the specified filename
        response = FileResponse(
            buffer, as_attachment=True, filename=filename)

        return response
    return render(request, 'common/Autogenerate.html')


def url(request):
    return render(request, 'common/URL.html')


def Download_file(request):
    url = request.POST.get('text_area')
    response = requests.get(url)
    if request.method == 'POST':
        if 'Download' in request.POST:
            try:
                # Download webpage

                # Parse webpage using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Inline all JS and CSS into HTML
                for script in soup(['script', 'link']):
                    if script.has_attr('src'):
                        # Download and replace external JS and CSS with inline JS and CSS
                        if script.name == 'script':
                            content = requests.get(script['src']).text
                            script.string = content
                            script.attrs = {}
                        elif script.name == 'link' and script['rel'] == ['stylesheet']:
                            content = requests.get(script['href']).text
                            style = soup.new_tag('style', type='text/css')
                            style.string = content
                            script.replace_with(style)

                # Minify HTML
                minified_html = htmlmin.minify(str(soup))

                # Create a file-like buffer to receive the minified HTML data
                buffer = io.BytesIO()
                buffer.write(minified_html.encode('utf-8'))
                buffer.seek(0)

                # Generate a file name for the minified HTML file
                filename = 'minified.html'

                # Create a FileResponse object with the minified HTML data and the specified filename
                response = FileResponse(
                    buffer, as_attachment=True, filename=filename)

                return response
            except:
                return HttpResponse("The code is not open scorce")
    return render(request, 'common/URL.html')


def edits(request):
    return render(request, 'common/Edit.html')
