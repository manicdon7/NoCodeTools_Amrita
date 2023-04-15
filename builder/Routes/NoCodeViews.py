from django.shortcuts import render
from django.http import JsonResponse
from ..models import Pages, ChatMessage
from django.core.serializers import serialize
import json
from .Tool.Tools import random_image
from .AI_Functions import Code_scriping
# Create your views here.


def index(request):
    pages = Pages.objects.all()
    return render(request, 'NoCodeBuilderPages/pages.html', {"pages": pages})


def addPage(request):
    return render(request, 'NoCodeBuilderPages/index.html')


def savePage(request):
    if (request.method == 'POST'):
        html = request.POST['html']
        css = request.POST['css']
        Project_name = request.POST['Project_name']
        page = Pages.objects.create(
            name=Project_name, html=html, css=css, image=random_image())
        page.save()
    return JsonResponse({"result": (json.loads(serialize('json', [page])))[0]})


def editPage(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'NoCodeBuilderPages/index.html', {"page": page})


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


<<<<<<< HEAD
def ResumeBuilder(request):
    if request.method == 'POST':
        my_field_value = request.POST.get('my_field')
        return render(request, 'NoCodeBuilderPages/resume_maker.html', {"page": my_field_value})
    return render(request, 'common\Resume_input.html')


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
=======
def autogenerate(request):
    return render(request, 'common/Autogenerate.html')

def url(request):
    return render(request, 'common/URL.html')

def edits(request):
    return render(request, 'common/Edit.html')
>>>>>>> 06cd32a1a9f8ec8f203608365d44ba29fa37d9e9
