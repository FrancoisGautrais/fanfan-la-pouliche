import json
from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from website.common.errors import ImageNotFound
from website.models import Image

from . import responses
from .responses import json_ok
from ..common import errors
from ..forms.image_form import UploaderForm
from .utils import route_handler


@route_handler(allowed=("GET", "POST"))
def list(request : HttpRequest):
    exif = False
    if request.method == "GET":
        if "exif" in request.GET:
            exif=request.GET["exif"]!=False and request.GET["exif"]!="false" and request.GET["exif"]!="False"

        data = Image.objects.filter(**request.GET["query"]) if "query" in request.GET else Image.objects.all()
    else:
        dd = request.POST if len(request.POST) else json.loads(request.body)
        if "exif" in dd:
            exif=dd["exif"]!=False and dd["exif"]!="false" and dd["exif"]!="False"
        data = Image.objects.filter(**dd["query"])
    return json_ok([ x.as_dict(exif) for x in data])

@route_handler(allowed=("PUT", "POST"))
def create(request : HttpRequest):
    form = UploaderForm(request.POST, request.FILES)
    image = Image.new(form)
    return responses.image_desc(image)

@route_handler(allowed=("GET","POST", "DELETE"))
def get(request : HttpRequest, uuid : str, size : str = Image.SIZE_M):
    try:
        if request.method=="GET":
            img = Image.objects.get(uuid=uuid)
        elif request.method=="POST":
            return edit(request, uuid)
        else:
            return remove(request, uuid)
    except Image.DoesNotExist as err:
        return responses.image_not_found(uuid)

    path : Path = img.get_image_path(size)
    if not path.is_file():
        return responses.file_not_found(path)
    name = img.name if img.name else img.uuid
    return responses.image(path, name)


@route_handler(allowed=("POST",))
def edit(request : HttpRequest, uuid : str):
    try:
        img = Image.objects.get(uuid=uuid)
    except Image.DoesNotExist as err:
        return responses.image_not_found(uuid)

    data = json.loads(request.body)
    if "name" in data: img.name = data["name"]
    if "description" in data: img.description = data["description"]
    if "tags" in data: img.set_tags(data["tags"])
    if "groups" in data: img.set_groups(data["groups"])
    img.save()
    return responses.image_desc(img)

@route_handler(allowed=("GET",))
def info(request : HttpRequest, uuid : str):
    try:
        img = Image.objects.get(uuid=uuid)
    except Image.DoesNotExist as err:
        return responses.image_not_found(uuid)
    return responses.image_desc(img, True)



@route_handler(allowed=("DELETE",))
def remove(request : HttpRequest, uuid : str):
    try:
        img = Image.objects.get(uuid=uuid)
    except Image.DoesNotExist as err:
        return responses.image_not_found(uuid)
    id, name = img.uuid, img.name
    img.delete()
    return json_ok("L'image '%s' (%s) a été supprimée" % (name, id))


urls = [
    path('', list),
    path('add', create),
    path('<str:uuid>/info', info),
    path('<str:uuid>/edit', edit),
    path('<str:uuid>/remove', remove),
    path('<str:uuid>', get),
    path('<str:uuid>/<str:size>', get)
]