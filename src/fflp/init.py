import os

os.environ["DJANGO_SETTINGS_MODULE"]="fflp.settings"
from django.conf import settings
from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

from website.models.pagebuilder import Page
from website.models.tag import Tag

if Page.get_page("/") is None:
    Page.objects.create(url="/")


public=list(Tag.objects.filter(name="public"))
if not public:
    Tag.create_non_editable(name="public", description="Affiche en miniature")
else:
    public[0].editable=False
    public[0].save()


accueil=list(Tag.objects.filter(name="accueil"))
if not accueil:
    Tag.create_non_editable(name="accueil", description="À afficher sur la une de la page d'accueil")
else:
    accueil[0].editable=False
    accueil[0].save()

