import json

from django.http import HttpRequest, HttpResponse

from website.common.mail import send_auto_email
from website.models.config import config
from website.views.utils import route_handler


@route_handler(allowed=("PUT", "POST"), logged=False)
def contact(request : HttpRequest):
    data = request.POST or json.loads(request.body)
    for contact in config.get("mail.contacts"):
        opts = {
            "smtp" : config.get("mail.smtp"),
            "username" : config.get("mail.username"),
            "email" : contact,
            "password" : config.get("mail.password")
        }
        send_auto_email(data["name"], data["email"], data["message"], opts)
    return HttpResponse(json.dumps({
        "code" : "Success",
        "data" : None,
        "message" : "Success"
    }), headers={"Content-Type" : "application/json"})