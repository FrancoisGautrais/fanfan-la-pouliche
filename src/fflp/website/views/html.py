import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from fflp import settings
from .utils import  route_handler
from website.common.js_dependencies import JsDpendencies
from ..forms.image_form import UploaderForm
from ..models import Tag, Group
from ..pagebuilder.pagebuilder import PageBuilder


@route_handler(allowed=("GET",))
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



@route_handler(allowed=("GET",))
def serve_main(request : HttpRequest):
    pb = PageBuilder.from_url("/")
    return HttpResponse(pb.generate())