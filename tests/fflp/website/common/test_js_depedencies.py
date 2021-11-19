import pytest
from fflp import settings
from website.common.js_dependencies import JsDpendencies, Node

class TestDependaenceies:

    def test_star(self):
        obj = JsDpendencies(settings.WWW_DIR, "js/index.js")
        print(obj.as_include_script(prefix="/static"))

    def test_js(self):
        obj = JsDpendencies(settings.WWW_DIR, "js/index.js")
        print(obj.as_include_script(prefix="/static"))