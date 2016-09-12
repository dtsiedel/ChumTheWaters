from django.conf.urls import patterns, include, url
from chumthewaters import views
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
admin.autodiscover()

#all of the urls on our site
urlpatterns = patterns('',
    #format: url(r'^name', views.name, name = 'index')
    url(r'^$', views.index, name='index'),
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'),permanent=False), name="favicon"),
    url(r'^summoner', views.summoner, name='summoner'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^chumscore', views.chumscore, name='chumscore'),
    url(r'^riot.txt', views.riot, name='riot.txt'),
)

urlpatterns += staticfiles_urlpatterns()
