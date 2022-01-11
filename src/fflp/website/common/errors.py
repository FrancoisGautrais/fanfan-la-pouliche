

class HttpCode:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406


class FflpException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        msg = "Erreur l'exception '%s' ne définie pas l'attribut de classe '%s'"
        if not hasattr(self, "HTTP_STATUS"):
            raise BadDefinitionException(msg % (type(self).__name__, "HTTP_STATUS"))
        if not hasattr(self, "CODE"):
            raise BadDefinitionException(msg % (type(self).__name__, "CODE"))


    @classmethod
    def get_status_code(cls):
        return cls.HTTP_STATUS

    @classmethod
    def get_code(cls):
        return cls.CODE

class BadDefinitionException(FflpException):
    HTTP_STATUS=400
    CODE="bad defintion"

class BadParameterException(FflpException):
    HTTP_STATUS=400
    CODE="bad parameter"

class NotFoundException(FflpException):
    HTTP_STATUS=404
    CODE="not found"

class ImageNotFound(NotFoundException):
    CODE="image not found"

class TagNotFound(NotFoundException):
    CODE="image not found"

class RecursiveReference(NotFoundException):
    HTTP_STATUS = 500
    CODE="recursive reference"

class Exists(NotFoundException):
    HTTP_STATUS = 400
    CODE="resource exist"


class ElementNotFoundException(NotFoundException):
    HTTP_STATUS=404
    CODE="template elment not found"