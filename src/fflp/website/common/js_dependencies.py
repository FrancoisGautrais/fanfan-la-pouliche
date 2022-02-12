import os.path
from pathlib import Path
import re

from fflp import settings
from . import errors

import logging
logger = logging.getLogger(__name__)

class Node:
    REGEX=re.compile(r"module\.load\(\s*[\"\'](?P<path>[\w /\-_.]+\*?)[\"\']\s*\)")
    REGEX_MODULE=re.compile(r"module\.exports")
    REGEX_MODULE_REGISTER=re.compile(r"Module\.register")
    EXCULDE_MODULE =  Path("/js/third-party/")

    def __init__(self, root_dir, path, context=None, is_module=False):
        self.is_module = is_module
        self.root_dir = root_dir
        self.context = context if context is not None else root_dir
        self.relpath = (path if isinstance(path, Path) else Path(path))
        if self.relpath.as_posix()[0] == "/":
            self.path = self.root_dir / Path(self.relpath.as_posix()[1:])
        else:
            self.path = self.context / self.relpath
        self.dependencies=[]
        self.path_from_root="/"+self.path.relative_to(self.root_dir).as_posix()
        self.module_path = os.path.normpath(self.path)[len(self.root_dir.as_posix())+1:-3].replace('/',".")
        if self.EXCULDE_MODULE.as_posix() not in self.path.as_posix():
            self._find_depenenceies()

    def __eq__(self, other):
        return self.path == other.path


    def as_dict(self, **kwargs):
        x = {
            "path" : self.path_from_root,
            "module_name" : self.module_path,
            "module" : 'type="module"' if self.is_module else ''
        }
        for k, v in kwargs.items():
            x[k]=v
        return x

    def module_to_path(self, module):
        is_abs = module[0]!='.'
        if not is_abs: module=module[1:]
        module = "/".join([ (name if name else "..")  for name in module.split('.')])
        if module[-1]!="*" and not module[-1].endswith(".js"): module+=".js"
        return (self.root_dir if is_abs else self.path.parent ) / Path(module)


    def _find_depenenceies(self):
        data = self.path.read_text(encoding="utf8")
        if re.findall(self.REGEX_MODULE, data):
            self.is_module = True
            if not re.findall(self.REGEX_MODULE_REGISTER, data):
                with open(self.path, "w") as f:
                    f.write("window['module'] = Module.register(\"%s\");\n" % self.module_path+data)

        ret = re.findall(Node.REGEX, data)
        for x in ret:
            self.dependencies.extend(self._nodes_from_path(self.module_to_path(x)))

    def _nodes_from_path(self, path):
        if isinstance(path, str): path=Path(path)

        if not path.is_file() and path.name != '*':
                msg = "%s" % (path) if settings.DEBUG else "$ROOT/%s" % (
                        1 + path[len(self.root_dir.as_posix()):])
                raise errors.NotFoundException("Fichier statique js inexistant : %s" % msg)

        if path.name == '*':
            out = []
            if path.parent.is_dir():
                for name in sorted(os.listdir(path.parent)):
                    p = path.parent / name
                    if p.is_file() and p.name.lower().endswith(".js"):
                        out.append( p)
                return [Node(self.root_dir, "/"+name.relative_to(self.root_dir).as_posix(), self.path.parent) for name in out]
            else:
                logger.error("Le dossier '%s' est introuvable" % path.parent)
                raise Exception()
                return []
        else:
            return [Node(self.root_dir, "/"+path.relative_to(self.root_dir).as_posix(), self.path.parent )]


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s (%s)" % (self.relpath, [x.relpath.as_posix() for x in self.dependencies])

class JsDpendencies:
    JS_INIT="<script>%s</script>" % (settings.BASE_DIR / "website" / "templates" / "module.js").read_text()
    def __init__(self, root_dir, path):
        self.path = path if isinstance(path, Path) else Path(path)
        self.root_dir = root_dir
        self.root = Node(root_dir, path, is_module=True)

    def prepend(self, data):
        self.root.prepend(data)

    def append(self, data):
        self.root.prepend(data)

    def as_list(self):
        stack = [self.root]
        tmp = []
        while stack:
            current = stack.pop()
            stack.extend(current.dependencies)
            tmp.append(current)
        out=[]
        for x in reversed(tmp):
            if not x in out:
                out.append(x)
        return out


    def as_include_script(self, relative_to=None, prefix=''):
        pattern="<script %(module)s src=\"%(prefix)s%(path)s\"></script>"
        module_register="<script>window['module']=Module.register('%(module_name)s');</script>"
        module_unregister="<script>window['module']=undefined;</script>"
        out = [ JsDpendencies.JS_INIT ]


        for file in self.as_list():
            if file.EXCULDE_MODULE.as_posix() in  file.path.as_posix():
                out.append(module_unregister)
            else:
                out.append(module_register % file.as_dict())

            out.append(pattern % file.as_dict(prefix=prefix))
            if file.EXCULDE_MODULE.as_posix() in  file.path.as_posix():
                out.append(module_register % file.as_dict())

        return "\n\t".join(out)
