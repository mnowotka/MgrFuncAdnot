from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import registration

from gui.views import UserTaskListView

from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    url(r'^$', 'apps.main.views.homepage', name='site-homepage'),
    (r'^$', redirect_to, {'url': '/list'}),
    (r'^adnots/$', 'gui.views.index'),
    (r'^service-status/$', 'gui.views.service_status'),
    (r'^list/$', UserTaskListView.as_view()),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),

    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

)

urlpatterns += staticfiles_urlpatterns()

