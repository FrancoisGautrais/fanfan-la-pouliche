import json
from pathlib import Path

from django.core.exceptions import ValidationError
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
from website.models.tag import Tag
from ..forms.tag_form import TagForm


@route_handler(allowed=("GET"))
def list(request : HttpRequest):
    return json_ok([
        k.as_dict() for k in Tag.objects.filter(parent=None)
    ])



@route_handler(allowed=("GET"))
def list_flat(request : HttpRequest):
    return json_ok(Tag.list())


@route_handler(allowed=("PUT", "POST"))
def create(request : HttpRequest):
    form = TagForm(json.loads(request.body))
    return json_ok(Tag.create(form).as_dict())



@route_handler(allowed=("GET"))
def images(request : HttpRequest, uuid : str):
    form = TagForm(json.loads(request.body))
    try:
        tag = Tag.objects.get(uuid=uuid)
    except Tag.DoesNotExist as err:
        return responses.tag_not_found(uuid)

    uuids = []
    curr = tag
    while curr:
        uuids.append(curr.uuid)


@route_handler(allowed=("POST"))
def edit(request : HttpRequest, uuid : str):
    form = TagForm(json.loads(request.body))
    try:
        tag = Tag.objects.get(uuid=uuid)
    except Tag.DoesNotExist as err:
        return responses.tag_not_found(uuid)


    tag.edit(form)
    return json_ok(tag.as_dict())


@route_handler(allowed=("GET"))
def remove(request : HttpRequest, uuid : str):
    try:
        tag = Tag.objects.get(uuid=uuid)
    except Tag.DoesNotExist as err:
        return responses.tag_not_found(uuid)

    id, name = tag.uuid, tag.name
    tag.delete()
    return json_ok("Le tag '%s' (%s) a été supprimé " % (name, id))


urls = [
    path('', list),
    path('add', create),
    path('list', list_flat),
    path('enumerate', lambda x: json_ok(Tag.enumerate())),
    path('<str:uuid>/images', images),
    path('<str:uuid>/edit', edit),
    path('<str:uuid>/', edit),
    path('<str:uuid>/remove', remove),
]