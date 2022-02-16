from django.http import HttpRequest

from website.common.errors import FflpException
from website.views.responses import json_not_allowed, json_exception, json_unauthorized, redirect

class NeedAuthException(Exception):
    pass

THRW_EXCEPTION = True

def check_auth(request):
    if not request.user.is_authenticated:
        raise NeedAuthException()

def route_handler(*args, **kwargs):
    ALLOWED=None
    LOGGED = kwargs.get("logged", True)
    REDIRECT = kwargs.get("redirect", None)
    if "allowed" in kwargs:
        if isinstance( kwargs["allowed"], str):  kwargs["allowed"]=  [kwargs["allowed"].upper()]
        ALLOWED= [ k.upper() for k in kwargs["allowed"]]


    def inner(func):
        def wrapper(*wargs, **wkwargs):
            request : HttpRequest = wargs[0]
            if ALLOWED and not request.method in ALLOWED:
                return json_not_allowed(request, ALLOWED)
            if LOGGED and not request.user.is_authenticated:
                if REDIRECT is not None:
                    return redirect(REDIRECT)
                else:
                    return json_unauthorized()

            try:
                return func(*wargs, **wkwargs)
            except FflpException as err:
                if THRW_EXCEPTION:
                    raise err
                return json_exception(err)
            except NeedAuthException as err:
                if REDIRECT is not None:
                    return redirect(REDIRECT)
                else:
                    return json_unauthorized()

        return wrapper

    return inner
