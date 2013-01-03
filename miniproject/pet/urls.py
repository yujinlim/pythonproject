from django.conf.urls import patterns, include, url
import pet.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#
	url(r'^list.html$', pet.views.PetListView.as_view(), name='list'),
	url(r'^(?P<pk>\d+)$', pet.views.SinglePetView.as_view(), name='onepet'),
	# url(r'^listall.html', "pet.views.test", name='list'),
    # Examples:
    # url(r'^$', 'miniproject.views.home', name='home'),
    # url(r'^miniproject/', include('miniproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
