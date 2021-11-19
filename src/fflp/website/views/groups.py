import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from website.common.errors import ImageNotFound
from website.models import Image, Group

from . import responses
from .responses import json_ok
from ..common import errors
from ..forms.group_form import GroupForm
from ..forms.image_form import UploaderForm
from .utils import route_handler


@route_handler(allowed=("GET"))
def list(request : HttpRequest):
    return json_ok([
        k.as_dict() for k in Group.objects.all()
    ])


@route_handler(allowed=("PUT", "POST"))
def create(request : HttpRequest):
    form = GroupForm(request.POST)
    return Group.create(form).as_dict()




@route_handler(allowed=("POST"))
def edit(request : HttpRequest, uuid : str):
    form = GroupForm(request.POST)
    try:
        group = Group.objects.get(uuid=uuid)
    except Group.DoesNotExist as err:
        return responses.group_not_found(form.cleaned_data["uuid"])


    img = Image.objects.get(uuid=uuid)
    group.edit(form)
    return json_ok(group.as_dict())


@route_handler(allowed=("GET"))
def remove(request : HttpRequest, uuid : str):
    form = GroupForm(request.POST)
    try:
        group = Group.objects.get(uuid=uuid)
    except Group.DoesNotExist as err:
        return responses.tag_not_found(form.cleaned_data["uuid"])

    id, name = group.uuid, group.name
    group.delete()
    return json_ok("Le group '%s' (%s) a été supprimé " % (name, id))



urls = [
    path('', list),
    path('add', create),
    path('<str:uuid>/edit', edit),
    path('<str:uuid>/remove', remove)
]