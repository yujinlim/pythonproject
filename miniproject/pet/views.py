# Create your views here.
import django.views.generic
import django.shortcuts
import pet.models
import datetime
import django.db
import assistedjson.views
import paginatedview.views
import django.template
import django.core.urlresolvers

# List of all pets
class PetListView (django.views.generic.View) :
	def get(self, request, *args):
		context = {}
		return django.shortcuts.render_to_response("pets/adminbase.html", context)

# Get single pet
class SinglePetView (django.views.generic.View) :
	def get(self, request, *args, **kwargs):
		primary_key = kwargs['pk']
		try:
			dog = pet.models.Pet.objects.filter(pk = primary_key)[0]
		except:
			 pass
		return django.shortcuts.render_to_response("pets/base.html", {'user':'dog'})

# Get list of pets
# assistedjson.views.LoginRequiredJsonView
class PetEntriesView(assistedjson.views.JsonView, paginatedview.views.PaginatedView):
	def get(self, request, *args, **kwargs):
		context = self.prepare_paginated_context(request)
		self._response.debug('done')
		self._response.html(django.template.loader.render_to_string("pets/entries_list.html", context))
		return self.respond()
		#django.shortcuts.render_to_response("pets/entries_list.html", context)

	
	def get_queryset(self, request):
		qs = pet.models.Pet.objects.all().select_related('species__name')
		if request.user.is_authenticated() and not request.user.is_admin():
			qs = qs.filter(author = request.user)
		return qs
		
class PetEditView(django.views.generic.UpdateView):
	model = pet.models.Pet
	template_name = "pets/pet_form.html"
	success_url = django.core.urlresolvers.reverse_lazy('pet:list')
		
