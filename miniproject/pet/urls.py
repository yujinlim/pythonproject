from django.conf.urls import patterns, include, url
import pet.views
import django.contrib.auth.decorators
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#
	url(r'^list.html$', django.contrib.auth.decorators.login_required(pet.views.PetListView.as_view()), name='list'),
	url(r'^(?P<pk>\d+)$', pet.views.SinglePetView.as_view(), name='onepet'),
	url(r'^entries$', pet.views.PetEntriesView.as_view(), name='entries'),
	url(r'^edit/(?P<pk>\d+)/?$', pet.views.PetEditView.as_view(), name='edit'),
	url(r'^insert$', pet.views.PetInsertView.as_view(), name='insert'),
	url(r'^test_insert$', pet.views.PetTestView.as_view(), name='test_insert'),
	url(r'^delete/(?P<pk>\d+)$', pet.views.PetDeleteView.as_view(), name="delete"),
	url(r'^species/$', pet.views.PetSpeciesView.as_view(), name="species"),
    url(r'^pets/$', pet.views.PetsView.as_view(), name="pets"),
	url(r'^roulette/$', pet.views.PetView.as_view(), name="pet")

	# url(r'^listall.html', "pet.views.test", name='list'),
    # Examples:
    # url(r'^$', 'miniproject.views.home', name='home'),
    # url(r'^miniproject/', include('miniproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
