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
from website.models.tag import Tag
from .group import Group
from ..common import errors
from ..common.errors import BadParameterException
from ..common.utils import arg, random_name
from fflp import  settings
from ..forms.image_form import UploaderForm
from PIL import Image as  PImage
from PIL import ExifTags
from .utils import get_id


def remove_if_empty(path : Path):
    if not path.is_dir(): return
    if not len(os.listdir(path)):
        os.rmdir(path)
        remove_if_empty(path.parent)

def jsonify(x):
    if isinstance(x, (int, float, str)) or x is None:
        return x
    if isinstance(x, (list, tuple)):
        return [jsonify(k) for k in x]
    if isinstance(x, dict):
        return {
            str(k): jsonify(v) for k,v in x.items()
        }
    if isinstance(x, bytes):
        return {
            "format" : "base64",
            "data": base64.b64encode(x).decode('ascii')
        }

    if isinstance(x, IFDRational):
        return {
            "denominator": x.denominator,
            "imag": x.imag,
            "numerator": x.numerator,
        }
    return {
        k: jsonify(getattr(x,k)) for k in filter(lambda x: not x.startswith("_"), dir(x))
    }

def get_exif(img : PImage):
    exifData = {}
    exifDataRaw = img._getexif()
    if not exifDataRaw: return {}
    for tag, value in exifDataRaw.items():
        decodedTag = ExifTags.TAGS.get(tag, tag)
        exifData[decodedTag] = jsonify(value)
    return exifData

class Image(models.Model):

    STATE_UNINITIALIZED : int = 0
    STATE_INITIALIZED : int = 1

    QUALITY = 95
    SIZE_S : str = "xs"
    SIZE_M : str = "m"
    SIZE_L : str = "l"
    SIZE_ORIGINAL : str = "original"
    SIZES: dict[str, int] = {
        SIZE_S : 128,
        SIZE_M : 768,
        SIZE_L : 1920,
        SIZE_ORIGINAL : -1
    }
    SIZES_STR : list[str] = ",".join(SIZES.keys())

    uuid = models.CharField(max_length=64, primary_key=True)
    name = models.TextField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    groups = models.ManyToManyField(Group)
    meta = models.TextField()
    year = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    state = models.IntegerField(default=STATE_UNINITIALIZED)
    sizes = models.TextField(default=SIZES_STR)
    creation_date = models.DateTimeField()

    def get_tags(self):
        return [ [x.uuid, x.name] for x in self.tags.all() ]

    def add_tags(self, tags):
        for k in tags:
            if isinstance(k, (list, tuple)): k = k[0]
            tag = Tag.objects.get(uuid=k)
            print(f"add tag {tag.name} {tag.uuid}")
            self.tags.add(tag)

    def remove_tags(self, tags):
        for k in tags:
            if isinstance(k, (list, tuple)): k = k[0]
            tag = Tag.objects.get(uuid=k)
            print(f"remove tag {tag.name} {tag.uuid}")
            self.tags.remove(tag)

    def set_tags(self, tags):
        self.tags.clear()

        if isinstance(tags, (int, str)): tags = [tags]
        for tag in tags:
            if isinstance(tag, tuple):
                for t in tag:
                    if isinstance(t, int):
                        tagid = t
                        break
            else:
                tagid = tag
            try:
                tag = Tag.objects.get(uuid=tagid)
                self.tags.add(tag)
            except Tag.DoesNotExist as err:
                raise errors.TagNotFound("Le tag '%s' est inconnu" % tagid, tagid, err)


    def set_groups(self, groups):
        self.groups.clear()
        if isinstance(groups, (int, str)): groups=[groups]
        for group in groups:
            if isinstance(group, tuple):
                for t in group:
                    if isinstance(t, int):
                        groupid=t
                        break
                else:
                    groupid = group
                try:
                    group = Group.objects.get(id=groupid)
                except Group.DoesNotExist as err:
                    raise errors.GroupNotFound("Le group '%s' est inconnu" % groupid, groupid, err)
                self.groups.add(group)




    def as_dict(self, with_exif=False):
        tmp = {
            "uuid" : self.uuid,
            "name" : self.name,
            "description" : self.description,
            "tags" : [(t.uuid, t.name) for t in self.tags.all()],
            "groups" : [(t.uuid, t.name) for t in self.groups.all()],
            "sizes" : self.sizes.split(","),
            "creation_date" : str(self.creation_date)
        }
        if with_exif:
            tmp["meta"] = json.loads(self.meta) if self.meta else {}
        return tmp

    def get_image_path(self, size = SIZE_M):
        return settings.IMAGE_DIR / size /  ("%04d" % self.year) /\
               ("%02d" % self.month) / ("%02d" % self.day) / (self.uuid+".jpg")

    def remove(self, remove_files=True):
        if remove_files:
            for size in self.sizes.split(","):
                path = self.get_image_path(size)
                path.unlink(missing_ok=True)
                remove_if_empty(path.parent)

        self.delete()


    def _initialize(self, form : UploaderForm):
        sizes = self.sizes.split(',')
        for size in sizes:
            path : Path = self.get_image_path(size)
            path.parent.mkdir(parents=True, exist_ok=True)

        original = self.get_image_path(Image.SIZE_ORIGINAL) if Image.SIZE_ORIGINAL in sizes else tempfile.mktemp()


        file = form.files["file"]
        with open(original, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        with PImage.open(original) as img:
            width, height = img.size
            ratio = width/height
            for size in sizes:
                if size==Image.SIZE_ORIGINAL: continue
                path = self.get_image_path(size)
                w, h = self.SIZES[size], self.SIZES[size]

                if width>height:
                    h/=ratio
                elif height>width:
                    w*=ratio

                img.resize((int(w),int(h))).save(path, quality=self.QUALITY)
        exif = get_exif(img)
        self.meta = json.dumps(exif)

        if Image.SIZE_ORIGINAL not in sizes:
            original.unlink()


        self.save()


    @staticmethod
    def new(form : UploaderForm):
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day

        if not form.is_valid():
            raise BadParameterException("Le formulaire d'envoie d'image est invalide", form.errors)

        data = form.cleaned_data

        args = {
            "uuid" : get_id(32),
            "name": data["name"],
            "description": data["description"],
            "year" : year,
            "month" : month,
            "day" : day,
            "meta" : "",
            "creation_date" : date
        }
        image =  Image.objects.create(**args)
        tags = data.get("tags") or []
        for tagid in tags:
            try:
                tag = Tag.objects.get(uuid=tagid)
                image.tags.add(tag)
            except Tag.DoesNotExist as err:
                raise errors.TagNotFound("Le tag '%s' est inconnu" % tagid, tagid, err)
        image._initialize(form)
        return image


