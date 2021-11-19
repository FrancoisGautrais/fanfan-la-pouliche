from django.core.exceptions import ValidationError
from django.db import models
from .utils import get_id
from ..forms.group_form import GroupForm


class Group(models.Model):

    uuid = models.CharField(max_length=64)
    name = models.TextField()
    description = models.TextField()
    is_public = models.BooleanField()


    def as_dict(self):
        return {
            "uuid" : self.uuid,
            "name" : self.name,
            "description" : self.description,
            "is_public" : self.is_public
        }

    @staticmethod
    def create(form : GroupForm):
        if not form.is_valid():
            raise ValidationError(form.errors)
        data = form.cleaned_data

        return Group.objects.create(**{
            "uuid":  get_id(32),
            "name": data["name"],
            "description": data["description"],
            "is_public" : data["is_public"]
        })

    def edit(self, form : GroupForm):
        if not form.is_valid():
            raise ValidationError(form.errors)
        data = form.cleaned_data
        self.name = data["name"]
        self.description = data["description"]
        self.is_public =  data["is_public"]
        self.save()



