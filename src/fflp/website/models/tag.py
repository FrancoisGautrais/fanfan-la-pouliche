from django.core.exceptions import ValidationError
from django.db import models
from .utils import get_id
from ..common import errors
from ..forms.tag_form import TagForm


class Tag(models.Model):
    uuid = models.CharField(max_length=64, primary_key=True)
    name = models.TextField()
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    @property
    def path(self):
        path=[]
        curr=self
        while curr:
            path.insert(0, curr.name)
            curr=curr.parent
        return ".".join(path)

    def as_dict(self, children=True):

        tmp = {
            "id" : self.id,
            "name" : self.name,
            "path" : self.path,
            "parent" : self.parent.id if self.parent else None,
        }

        if children: tmp["children"] = [x.as_dict() for x in Tag.objects.filter(parent=self)]
        return tmp

    @staticmethod
    def list_path():
        return [
            [x.uuid, x.path] for x in Tag.objects.all()
        ]

    @staticmethod
    def create(form : TagForm):
        if not form.is_valid():
            raise ValidationError(form.errors)
        data = form.cleaned_data

        return Tag.objects.create(**{
            "uuid":  get_id(32),
            "name": data["name"],
            "description": data["description"],
            "parent" :  Tag.objects.get(uuid=data["parent"])
        })

    def edit(self, form : TagForm):
        if not form.is_valid():
            raise ValidationError(form.errors)
        data = form.cleaned_data
        self.name = data["name"]
        self.description = data["description"]
        self.parent =  Tag.objects.get(uuid=data["parent"])
        self.save()




