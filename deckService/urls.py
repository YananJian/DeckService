"""deckService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from core.utils import Util
from core.cache import Cache

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/(?P<username>\w{0,50})/decks$', 'core.controller.get_decks'),
    url(r'^users/(?P<username>\w{0,50})/detailed_decks$', 'core.controller.get_detailed_decks'),
    url(r'^decks/(?P<deckid>\d{0,50})/$', 'core.controller.get_specified_deck'),
]

Util.generate_decks_multi_pages()
c = Cache()
