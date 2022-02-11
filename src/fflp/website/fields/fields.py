from django.forms import CharField, Textarea



class ListStrField(CharField):
    widget = Textarea

    def to_python(self, value):
        if self.disabled:
            return value
        if value in self.empty_values:
            return None
        elif isinstance(value, (str)):
            return value.split(",") if value else []
        return None

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        return data.split(",") if data else []

    def prepare_value(self, value):
        return ",".join(value)

    def has_changed(self, initial, data):
        if super().has_changed(initial, data):
            return True
        # For purposes of seeing whether something has changed, True isn't the
        # same as 1 and the order of keys doesn't matter.
        return initial !=  self.to_python (data)


class TagsField(ListStrField):

    def to_python(self, value):
        from website.models import Tag
        ret = super().to_python(value)
        if isinstance(ret, (list)):
            return [Tag.objects.get(uuid=x) for x in ret]
        return ret

    def prepare_value(self, value):
        return ",".join([v.uuid for v in value])


    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        return self.to_python(data)