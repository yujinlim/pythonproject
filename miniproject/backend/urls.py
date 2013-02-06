from django.conf.urls import patterns, include, url
import backend.views
import django.views.decorators.http


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#
	url(r'^login.html$', backend.views.LoginView.as_view(), name="adminlogin"),
	url(r'^login/$', django.views.decorators.http.require_POST(backend.views.LoginView.as_view()), name="adminlogin.action")
    # Examples:
    # url(r'^$', 'miniproject.views.home', name='home'),
    # url(r'^miniproject/', include('miniproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
