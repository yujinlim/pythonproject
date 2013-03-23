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
import django.core
import django.core.serializers
import django.contrib.messages
import django.http
import django.core.context_processors


class PetsView(assistedjson.views.JsonView):
    def get(self, request, *args, **kwargs):
        #data = django.core.serializers.serialize("json", pet.models.Pet.objects.all() )
        qs = pet.models.Pet.objects.all()
        context = list(qs)
        context = map(lambda x: x.toDict(), context)
        self._response.data(key="pets", value=context)
        self._response.debug('done')
        return self.respond()

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
        print("context here ==>")
        print(context)
        self._response.debug('done')
        self._response.html(django.template.loader.render_to_string("pets/entries_list.html", context))
        print("rendered")
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
    # form_class = pet.forms.PetForm()
    # Below is generic view
    # model = pet.models.Pet
    template_name = "pets/pet_form.html"
    success_url = django.core.urlresolvers.reverse_lazy('pet:list')
    
    def get(self, request, *args, **kwargs):
        pet_object = pet.models.Pet.objects.get(id = self.kwargs['pk'])
        pet_form = pet.forms.PetForm(instance=pet_object)
        pet_form.id = self.kwargs['pk']
        pet_videos = list(pet_object.videos.all())
        pet_video_forms = []
        for pet_video in pet_videos:
            pet_video_forms.append(pet.forms.PetVideoForm(instance=pet_video))
        context = {'form': pet_form, 'video_forms':pet_video_forms}
        print(context)
        return django.shortcuts.render_to_response(self.template_name, context )
    
#    def get_object(self, queryset=None):
#        print("get object first")
#        pet_object = pet.models.Pet.objects.get(id = self.kwargs['pk'])
#        # pet_video_object = pet_object.video.all()
#        return pet_object

# Insert new pet
class PetInsertView(django.views.generic.View):
    # success_url = django.core.urlresolvers.reverse_lazy('pet:list')
    
    def get(self, request, *args, **kwargs):
        """ get form for insert pet """
        pet_form = pet.forms.PetForm()
        pet_video_form = pet.forms.PetVideoForm()
        print(pet_form, pet_video_form)
        context = {'pet_form': pet_form,'pet_video_form': pet_video_form}
        context.update(django.core.context_processors.csrf(request))
        return django.shortcuts.render_to_response('pets/pet_insert.html', context)

    def post(self, request, *args, **kwargs):
        """ insert pet """
        pet_form = pet.forms.PetForm(request.POST)
        pet_videos = json.loads(request.POST['videos'])
        # pet_video_form = pet.forms.PetVideoForm(request.POST)
#        
#        for pet_video in pet_videos:
#            print(type(pet_video))
#            video = pet.models.PetVideo(pet_video)
#            print(video.video_link)
#        # videos = pet.models.PetVideo(pet_videos)
#        # print(videos)
#        print(request.POST)
#        print(type(pet_videos))
        # print(request.POST)
        # print(pet_form, pet_video_form)
        
        if pet_form.is_valid():
            print("is valid")
            new_pet_form = pet_form.save()
            for pet_video in pet_videos:
                pet_video_form = pet.forms.PetVideoForm(pet_video)
                if pet_video_form.is_valid():
                    instance = pet_video_form.save(commit=False)
                    print(instance.created_by_id)
                    if instance.created_by_id == None:
                        instance.created_by_id = request.user.id
                    if instance.pet_id == None:
                        instance.pet = new_pet_form
                    instance.save()
                    print("instance in saved")
                else:
                    for error in pet_video_form.errors:
                        print(error)
                        django.contrib.messages.error(request, error)
                    print("error in saving videos")
                    return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:insert'))
            return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:list'))
        else:
            print("not valid")
            for error in pet_form.errors:
                print(error)
                django.contrib.messages.error(request, error)
            print(request)
            return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:insert'))
#    form_class = pet.forms.PetForm
#    model = pet.models.Pet
#    template_name = "pets/pet_insert.html"
#    success_url = django.core.urlresolvers.reverse_lazy('pet:list')
#    
#    def get_context_data(self, **kwargs):
#        context = super(PetInsertView, self).get_context_data(**kwargs)
#        context["petvideo_form"] = pet.forms.PetVideoForm()
#        context["videos"] = []
#        return context
#    
#    def post(self, request, *args, **kwargs):
#        form = pet.forms.PetForm(request.POST)
#        if form.is_valid():
#            form.save()
#        else:
#            #return
#            for error in form.errors:
#                django.contrib.messages.error(request, error)
#            return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:insert'))
#        if not self.save_videos(request):
#            for error in form.errors:
#                django.contrib.messages.error(request, error)
#        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:list'))
#        

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
    
class PetTestView(django.views.generic.View):
    pass
    
        
