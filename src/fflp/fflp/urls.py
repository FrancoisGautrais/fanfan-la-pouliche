"""fflp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from fflp import settings
from website.views import html, images, tags, groups
urlpatterns = [
    path('admin/', admin.site.urls),
    path("image/", include(images.urls)),
    path("tag/", include(tags.urls)),
    path("group/", include(groups.urls)),
    path("", html.serve_main),
    path("admin", html.serve_admin),
    path("page", html.serve_admin)
]  #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
