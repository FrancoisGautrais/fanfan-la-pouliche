from pathlib import Path
from datetime import datetime
from django.db import models
from .tag import Tag
from .visibility import Visibility
from ..common.utils import arg, random_name
from fflp import settings


class Image(models.Model):
    name = models.TextField()
    description = models.TextField()
    path = models.TextField()
    tags = models.ManyToManyField(Tag)
    visibility = models.ManyToManyField(Visibility)


    def remove(self):
        path : Path = settings.IMAGE_DIR / self.path
        path.unlink()
        self.delete()

    def new(self, **kwargs):
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day

        args = {
            "name": arg(kwargs, "name", empty=True)
            "description": arg(kwargs, "description")
            "path": "%04d/%02d/%02d/%s.jpg" % (year, month, day, random_name())
        }
        return Image.object.create(**args)

