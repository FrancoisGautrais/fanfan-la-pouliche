import json
import sys
from collections import defaultdict

from django.contrib.auth import logout, authenticate, login
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import path

from website.views import responses
from website.views.utils import route_handler


@route_handler(allowed=("POST"), logged=False)
def serve_login(request : HttpRequest):
    if request.method == "POST":
        params = request.POST or  json.loads(request.body)
        user = authenticate(request, username=params["username"], password=params["password"])
        if user is not None:
            login(request, user)
            return responses.redirect( request.GET["redirect"] if "redirect" in request.GET else "/")
        return responses.json_unauthorized()

@route_handler(allowed=("GET"))
def serve_logout(request : HttpRequest):
    logout(request)
    return HttpResponseRedirect("/login")

urls=[
    path('login', serve_login),
    path('logout', serve_logout),
]