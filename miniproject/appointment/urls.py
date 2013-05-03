from django.conf.urls import patterns, include, url
import appointment.views
import django.contrib.auth.decorators
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #
    url(r'^list/$', django.contrib.auth.decorators.login_required(appointment.views.AppointmentListView.as_view()), name='list'),
    url(r'^entries$', appointment.views.AppointmentEntriesView.as_view(), name='entries'),
    url(r'^update/(?P<pk>\d+)/?$', appointment.views.AppointmentUpdateView.as_view(), name='update'),
    url(r'^insert/$', appointment.views.AppointmentInsertView.as_view(), name='insert')

)