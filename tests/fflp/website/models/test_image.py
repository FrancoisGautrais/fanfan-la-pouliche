import pytest
from django.test import Client
from fflp.settings import TESTS_DIR
from website.models.image import get_id, Image


def decorator(*args, **kwargs):
    if "arg" in kwargs:
        print("arg")

    def inner(func):
        def wrapper(*wargs, **wkwargs):
            print(wargs, wkwargs)
            return func
        # code functionality here
        print("Inside inner function")
        print("I like", args, kwargs)

        return wrapper

    # reurning inner function
    return inner

@decorator("salut", "ok", x=1)
def mymeth(arg):
    print(arg)

class TestImage:

    def test_get_id(self):
        mymeth("argument")
        assert len(get_id(23)) == 23
        assert len(get_id(64)) == 64
        print("\n\n%s\n\n" % TESTS_DIR)


    def test_upload(self):
        c = Client()
        path = TESTS_DIR / "ressources" / "images" / "lena_landscape_hq.jpg"
        with open(path, "rb") as f:
            c.post()
