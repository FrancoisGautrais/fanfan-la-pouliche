import json
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from fflp import settings
from .utils import  route_handler
from website.common.js_dependencies import JsDpendencies
from ..forms.image_form import UploaderForm
from ..models import Tag, Group
from ..pagebuilder.pagebuilder import PageBuilder
from website.models.stats import Stat

@route_handler(allowed=("GET",), redirect="/login")
def serve_admin(request : HttpRequest):
    dep = JsDpendencies(settings.WWW_DIR, "js/index.js")
    data={
        "tags": Tag.enumerate(),
        "groups" : { x.uuid: x.as_dict() for x in  Group.objects.all()}
    }
    return render(request, 'index/index.html', {
        "form" : UploaderForm(),
        "include_script" : dep.as_include_script(prefix=settings.STATIC_URL),
        "bootstrap_data" : json.dumps(data)
    })


@route_handler(allowed=("GET",), logged=False)
def serve_login(request : HttpRequest):
    return render(request=request, template_name="index/login.html")

@route_handler(allowed=("GET",), logged=False)
def serve_main(request : HttpRequest):
    pb = PageBuilder.from_url("/")
    if request.session.session_key is None:
        request.session.save()
    Stat.from_request(request)
    return HttpResponse(pb.generate())

