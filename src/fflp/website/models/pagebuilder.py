import base64
import json
import os
import random
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from PIL.TiffImagePlugin import IFDRational
from django.db import models
from .tag import Tag
from .group import Group
from ..common import errors
from ..common.errors import BadParameterException
from ..common.utils import arg, random_name
from fflp import  settings
from ..forms.image_form import UploaderForm
from PIL import Image as  PImage
from PIL import ExifTags
from .utils import get_id

class Page(models.Model):

    url = models.TextField(unique=True)
    content = models.TextField(default="{}")


    @staticmethod
    def set_page(url, content):
        try:
            page = Page.objects.get(url=url)
        except Page.DoesNotExist:
            page = Page.objects.create(url=url)

        page.content = json.dumps(content)
        page.save()


    @staticmethod
    def get_page(url):
        try:
            return Page.objects.get(url=url)
        except Page.DoesNotExist:
            return None

