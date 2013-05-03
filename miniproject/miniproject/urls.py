from django.conf.urls import patterns, include, url
import backend.views
import django.views.decorators.http

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#
	url(r'^pet/', include('pet.urls',namespace ="pet")),
	url(r'^backend/', include('backend.urls', namespace="backend")),
	# url(r'^/', include('frontend.urls', namespace="frontend")),
	url(r'^api/', include('api.urls', namespace="api")),
	url(r'^organization/', include('organization.urls', namespace="organization")),
	url(r'^appointment/', include('appointment.urls', namespace="appointment"))	
	
    # Examples:
    # url(r'^$', 'miniproject.views.home', name='home'),
    # url(r'^miniproject/', include('miniproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
