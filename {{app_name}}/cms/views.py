from shutil import move
import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from common.helpers import jsonify, resolve_http_method

from {{app_name}} import settings
from cms.helpers import nav
from cms.models import Page, UploadedMedia, MediaCollection
from cms import page_data

def get_page_data(name):
    #replace dash with underscores because functions can't have dashes in them
    name = name.replace('-','_')

    if hasattr(page_data, name):
        return getattr(page_data, name)()
    return None

def update_page_data(page_name, page_context):
    new_page_data = get_page_data(page_name)
    if new_page_data is not None: 
        page_context.update(new_page_data)
    return page_context

def standard_context():
    return { 'nav': nav, 'app_name' : settings.SITE_NAME }

def index(request):
    c = update_page_data('index', standard_context())
    return render(request,'index.html' , c)

def page(request, page_slug):
    c = update_page_data('index', standard_context())
    print c
    c.update({
        'page': Page.objects.get(slug=page_slug, active=True),
    })
    return render(request, 'pages/single.html', c)

def post(request, post_id):
    pass 

def posts(request):
    pass

def media_list(request, list_id ):
    collection = MediaCollection.objects.get(pk=list_id)
    return render(request, 'pages/media_collection.html', {"collection":collection})

def media(request, id):
    media = UploadedMedia.objects.get(pk=id)
    return render(request, 'pages/media.html', {"media": media })

@csrf_exempt
def upload(request):
    def post():
        uploaded = UploadedMedia.objects.create( 
                filename = "NA", 
                file = request.FILES['file'])

        return jsonify({"filename": uploaded.file.name, "filelink": uploaded.file.url})

    return resolve_http_method(request, [post])
