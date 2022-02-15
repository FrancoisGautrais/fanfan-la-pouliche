import datetime

from django.db import models
from django.http import HttpRequest

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Stat(models.Model):

    date = models.DateTimeField(default=None)
    ip = models.TextField()
    session = models.TextField()


    @staticmethod
    def from_request(request : HttpRequest):
        ip = get_client_ip(request)
        return Stat.objects.create(
            date = datetime.datetime.now(),
            ip = ip,
            session = request.session.session_key
        )
