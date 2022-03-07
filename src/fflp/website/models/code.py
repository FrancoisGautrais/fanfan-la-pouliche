import uuid
from datetime import datetime
from pathlib import Path
import random
from django.conf import settings
from django.db import models

from website.common.errors import BadParameterException
from website.forms.image_form import UploaderCodeForm

class Code(models.Model):
    objects : models.Manager
    code : str = models.CharField(max_length=256, unique=True)
    path : str = models.TextField()
    dl_count : int = models.IntegerField(default=0)
    comment : str = models.TextField()

    @staticmethod
    def new_code(n=8):
        return [random.choice("abcdefghijkmnpqrstuvwxyz123456789-") for _ in range(n)]

    @staticmethod
    def create(form : UploaderCodeForm):
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day


        if not form.is_valid():
            raise BadParameterException("Le formulaire d'envoie d'image est invalide", form.errors)

        data = form.cleaned_data

        file = form.files["file"]


        filename = str(uuid.uuid4())+"_"+file.filename

        path = Path("code") / ("%04d" % year) /\
               ("%02d" % month) / ("%02d" % day) / filename
        with open(path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        args = {
            "code": data["code"] or Code.new_code(),
            "comment": data["comment"],
            "path" : data["path"],
            "dl_count" : 0
        }
        return Code.objects.create(**args)

    @staticmethod
    def get(code):
        try:
            return Code.objects.get(code=code)
        except Code.DoesNotExist:
            return None


    @staticmethod
    def download(code):
        x = Code.get(code)
        if x is None:
            return None
        x.dl_count+=1
        x.save()
        return x






