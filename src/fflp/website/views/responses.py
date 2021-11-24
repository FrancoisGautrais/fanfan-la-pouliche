import json
from pathlib import Path

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpRequest

from fflp import settings
from website.common import errors
from website.models import Image
from website.common.errors import HttpCode, FflpException


IMAGE_NOT_FOUND = "image_not_found"
TAG_NOT_FOUND = "tag_not_found"
GROUP_NOT_FOUND = "group_not_found"
FILE_NOT_FOUND = "file_not_found"
HTTP_ERROR = "http_error"

def json_response(data, code = "ok", message : str = "Success", http_code=HttpCode.OK):
    return HttpResponse(json.dumps({
        "data" : data,
        "code" : code,
        "message" : message
    }), content_type="application/json", status=http_code)


def json_ok(data):
    return json_response(data)

def json_created(data):
    return json_response(data, http_code=HttpCode.CREATED)

def image_not_found(uuid : str):
    return json_response(None, IMAGE_NOT_FOUND, "L'image d'id '%s' est introuvable" % uuid, HttpCode.NOT_FOUND)

def tag_not_found(uuid : str):
    return json_response(None, TAG_NOT_FOUND, "Le tag d'id '%s' est introuvable" % uuid, HttpCode.NOT_FOUND)

def group_not_found(uuid : str):
    return json_response(None, GROUP_NOT_FOUND, "Le group d'id '%s' est introuvable" % uuid, HttpCode.NOT_FOUND)

def file_not_found(path : Path):
    msg = "Le fichier '%s' est introuvable" % (path if settings.DEBUG else path.name)
    return json_response(None, IMAGE_NOT_FOUND, msg, HttpCode.NOT_FOUND)

def image_desc(image : Image, exif=False):
    return json_ok(image.as_dict(exif))

def json_not_allowed(request : HttpRequest, allowed=None):
    url, current = request.path, request.method
    msg = "Méthode '%s' non autorisée sur '%s'" % (current, url)
    if allowed: msg+=" (autorisée : %s)" % str(allowed)
    return json_response(None, HTTP_ERROR, msg, HttpCode.METHOD_NOT_ALLOWED)



def _format_exc(exc):
    return json.dumps(str(exc))


def json_exception(err : Exception):
    if isinstance(err, errors.FflpException):
        return json_response(_format_exc(err), err.get_code(), str(err), err.get_status_code())
    else:
        raise errors.BadDefinitionException("Impossible de sérialiser l'exception", err)

def exception(err : Exception):
    return json_exception(err)

def image(path, name):
    with open(path, "rb") as f:
        data = f.read()
    resp = HttpResponse(data, content_type="image/jpeg")
    resp['Content-Disposition'] = 'attachment; filename="%s.jpg"' % name
    return resp


def redirect(url, permanent=False):
    if permanent:
        return HttpResponsePermanentRedirect(url)
    else:
        return HttpResponseRedirect(url)