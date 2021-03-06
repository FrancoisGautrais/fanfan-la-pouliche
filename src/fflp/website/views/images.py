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
from .utils import route_handler, check_auth


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

@route_handler(allowed=("GET","POST", "DELETE"), logged=False)
def get(request : HttpRequest, uuid : str, size : str = Image.SIZE_M):
    try:
        if request.method=="GET":
            img = Image.objects.get(uuid=uuid)
        elif request.method=="POST":
            check_auth(request)
            return edit(request, uuid)
        else:
            check_auth(request)
            return remove(request, uuid)
    except Image.DoesNotExist as err:
        return responses.image_not_found(uuid)

    if size == Image.SIZE_ORIGINAL:
        check_auth(request)
    path : Path = img.get_image_path(size)
    if not path.is_file():
        return responses.file_not_found(path)
    name = img.name if img.name else img.uuid
    return responses.image(path, name, request.GET.get("download", "false")=="true")


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
    img.remove()
    return json_ok("L'image '%s' (%s) a ??t?? supprim??e" % (name, id))


@route_handler(allowed=("GET","POST", "PUT", "DELETE"), logged=False)
def tags(request : HttpRequest, uuid : str):
    try:
        img = Image.objects.get(uuid=uuid)
        if request.method=="GET":
            return json_ok(img.get_tags())
        elif request.method in ("POST", "PUT"):
            check_auth(request)
            tags = request.POST or json.loads(request.body)
            print(f"add tag {tags}")
            img.add_tags(tags)
            img.save()
            return json_ok(tags)
        else:
            check_auth(request)
            tags = request.POST or json.loads(request.body)
            img.remove_tags(tags)
            img.save()
            return json_ok(tags)
    except Image.DoesNotExist as err:
        return responses.image_not_found(uuid)




urls = [
    path('', list),
    path('add', create),
    path('<str:uuid>/info', info),
    path('<str:uuid>/edit', edit),
    path('<str:uuid>/tags', tags),
    path('<str:uuid>/remove', remove),
    path('<str:uuid>', get),
    path('<str:uuid>/<str:size>', get),
]