import os
from pathlib import Path

for module in ["%s.%s" % (__name__, x) for x in os.listdir(Path(__file__).parent)]:
    if module.endswith("py") and not module.endswith("__init__.py") and not module.endswith("utils.py"):
        print(module[:-3])
        __import__(module[:-3])
