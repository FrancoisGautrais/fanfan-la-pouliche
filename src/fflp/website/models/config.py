import json

from django.db import models


class ConfigEntry(models.Model):

    key = models.TextField(unique=True)
    value = models.TextField(default=None, null=True)

    @staticmethod
    def get(k, default=None):
        try:
            return json.loads(ConfigEntry.objects.get(key=k).value)
        except ConfigEntry.DoesNotExist:
            return default

    @staticmethod
    def set(k, v, erase=True):
        try:
            set = ConfigEntry.objects.get(key=k)
            if not erase: return
            set.value=json.dumps(v)
            set.save()
        except ConfigEntry.DoesNotExist:
            ConfigEntry.objects.create(key=k, value=json.dumps(v))


class _Config:
    def __init__(self):
        self._cache={}

    def get(self, item, default=None):
        return self._cache.get(item, ConfigEntry.get(item, default))

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value, erase=True):
        self._cache[key]=value
        ConfigEntry.set(key, value, erase)

    def _load(self, data, erase=True):
        def _load(key, d, prefix=None):
            prefix =  (prefix+"."+key) if prefix else key
            if isinstance(d, dict):
                for k, v in d.items():
                    _load(k, v, prefix)
            elif isinstance(d, (str, int, float, bool, list)) or d is None:
                self.set(prefix, d, erase)
            else:
                raise Exception(f"Error at {prefix}: type {d.__class__.__name__} is not allow in settings")
        assert isinstance(data, dict)
        _load(None, data)

    def load(self, data):
        return self._load(data, True)

    def load_default(self, data):
        return self._load(data, False)

    def dump(self):
        def _set(root, path, data):
            path = path.split(".")
            curr=root
            while len(path)>=1:
                next = path.pop(0)
                if next not in curr:
                    curr[next]={}
            next = path.pop(0)
            curr[next]=data
        out={}
        for k, v in ConfigEntry.objects.all():
            tmp=json.loads(v)
            self._cache[k]=tmp
            _set(out, k, tmp)

        return out


config = _Config()