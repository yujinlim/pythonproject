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
import pet.forms
import json

# List of all pets
class PetListView (django.views.generic.View) :
	def get(self, request, *args):
		context = {'page_title':'List Of Pets'}
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
class PetEntriesView(assistedjson.views.LoginRequiredJsonView, paginatedview.views.PaginatedView):
	def get(self, request, *args, **kwargs):
		context = self.prepare_paginated_context(request)
		self._response.debug('done')
		self._response.html(django.template.loader.render_to_string("pets/entries_list.html", context))
		return self.respond()
		#django.shortcuts.render_to_response("pets/entries_list.html", context)

	def get_queryset(self, request):
		qs = pet.models.Pet.objects.all().select_related('species__name')
		if request.user.is_authenticated() and not request.user.is_superuser:
			qs = qs.filter(author = request.user)
		return qs
	
	def per_page(self):
		return 5
		
# Edit pet
class PetVideoInsert():
	def save_videos(self, request):
		self.errors = []
		videos = json.loads(request.POST.get("videos", "[]"))
		for video in videos:
			form = pet.forms.PetVideoForm(video)
			if form.is_valid():
				video = form.save()
			else:
				self.errors = self.errors + form.errors
		return self.errors.__len__() == 0
		
		
class PetEditView(django.views.generic.UpdateView):
	form_class = pet.forms.PetForm
	#Below is generic view
	model = pet.models.Pet
	template_name = "pets/pet_form.html"
	success_url = django.core.urlresolvers.reverse_lazy('pet:list')

# Insert new pet
class PetInsertView(django.views.generic.CreateView, PetVideoInsert):
	form_class = pet.forms.PetForm
	model = pet.models.Pet
	template_name = "pets/pet_insert.html"
	success_url = django.core.urlresolvers.reverse_lazy('pet:list')
	
	def get_context_data(self, **kwargs):
		context = super(PetInsertView, self).get_context_data(**kwargs)
		context["petvideo_form"] = pet.forms.PetVideoForm()
		context["videos"] = []
		return context
	
	def post(self, request, *args, **kwargs):
		form = pet.forms.PetForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			#return
			for error in form.errors:
				django.contrib.messages.error(request, error)
			return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:insert'))
		if not self.save_videos(request):
			for error in form.errors:
				django.contrib.messages.error(request, error)
		return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:list'))
		
class PetDeleteView(django.views.generic.View):
	def get(self, request, *args, **kwargs):
		primary_key = kwargs['pk']
		try:
			pet.models.Pet.objects.get(pk=primary_key).delete()
		except:
			pass
		return django.shortcuts.redirect('pet:list') #("pets/adminbase.html")

class PetSpeciesView(assistedjson.views.LoginRequiredJsonView):
	def post(self, request, *args, **kwargs):
		species = request.POST.get('species', None)
		context = pet.models.Race.objects.filter(species_id = species)
		self._response.html(django.template.loader.render_to_string("pets/races_list.html", {'races' : context}))
		return self.respond()
		
