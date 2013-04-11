from django.conf.urls import patterns, include, url
import organization.views
import django.contrib.auth.decorators
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #
    url(r'^list.html$', django.contrib.auth.decorators.login_required(organization.views.OrganizationListView.as_view()), name='list'),
#    url(r'^(?P<pk>\d+)$', organization.views.SinglePetView.as_view(), name='onepet'),
    url(r'^entries$', organization.views.OrganizationEntriesView.as_view(), name='entries'),
#    url(r'^edit/(?P<pk>\d+)/?$', organization.views.PetEditView.as_view(), name='edit'),
#    url(r'^yuser$', organization.views.OrganizationYouTubeUser.as_view(), name='youtube_user'),
    url(r'^insert/$', organization.views.OrganizationInsertView.as_view(), name='insert'),
#    # url(r'^test_insert$', organization.views.PetTestView.as_view(), name='test_insert'),
#    url(r'^delete/(?P<pk>\d+)$', organization.views.PetDeleteView.as_view(), name="delete")
    # url(r'^listall.html', "pet.views.test", name='list'),
    # Examples:
    # url(r'^$', 'miniproject.views.home', name='home'),
    # url(r'^miniproject/', include('miniproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)