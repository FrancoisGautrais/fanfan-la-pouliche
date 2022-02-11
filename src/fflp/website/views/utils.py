from django.http import HttpRequest

from website.common.errors import FflpException
from website.views.responses import json_not_allowed, json_exception

THRW_EXCEPTION = True
def route_handler(*args, **kwargs):
    ALLOWED=None
    if "allowed" in kwargs:
        if isinstance( kwargs["allowed"], str):  kwargs["allowed"]=  [kwargs["allowed"].upper()]
        ALLOWED= [ k.upper() for k in kwargs["allowed"]]

    def inner(func):
        def wrapper(*wargs, **wkwargs):
            request : HttpRequest = wargs[0]
            if ALLOWED and not request.method in ALLOWED:
                return json_not_allowed(request, ALLOWED)

            try:
                return func(*wargs, **wkwargs)
            except FflpException as err:
                if THRW_EXCEPTION:
                    raise err
                return json_exception(err)

        return wrapper

    return inner
