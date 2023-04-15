from django.shortcuts import render
from django.http import JsonResponse
from ..models import Pages
from django.core.serializers import serialize
import json
from .Tool.Tools import random_image
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


def autogenerate(request):
    return render(request, 'common/Autogenerate.html')

def url(request):
    return render(request, 'common/URL.html')

def edits(request):
    return render(request, 'common/Edit.html')