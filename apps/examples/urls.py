from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to, direct_to_template


urlpatterns = patterns('',
    url(r'^email/$', 'views.email'),
)