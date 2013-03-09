from django.conf.urls import patterns, include, url
import api.views
import django.contrib.auth.decorators   
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^random/$', api.views.RandomApi.as_view(), name="random"),
    url(r'^next/$', api.views.NextApi.as_view(), name="next"),
    url(r'^details/$', api.views.DetailApi.as_view(), name="detail"),
    url(r'^appointment/$', api.views.AppointmentApi.as_view(), name="appointment"),
    url(r'^donate/$', api.views.DonationApi.as_view(), name="donation")

    # url(r'^listall.html', "pet.views.test", name='list'),
    # Examples:
    # url(r'^$', 'miniproject.views.home', name='home'),
    # url(r'^miniproject/', include('miniproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
