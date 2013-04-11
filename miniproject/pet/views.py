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
class PetVideos():
    pass
        
class PetInsertView(django.views.generic.View):
    # success_url = django.core.urlresolvers.reverse_lazy('pet:list')
    
    def get(self, request, *args, **kwargs):
        """ get form for insert pet """
#        print(request.user.organization.youtube_channel)
#        return None
        pet_form = pet.forms.PetForm()
        pet_form.channel = request.user.organization.youtube_channel
        pet_video_form = pet.forms.PetVideoForm()
        storage = django.contrib.messages.get_messages(request)
        for message in storage:
            print(message)
            print(type(message))
            # message[3] = message[3].replace('_', ' ')
        storage.used = True
        context = {'pet_form': pet_form,'pet_video_form': pet_video_form, 'messages' : storage}
        context.update(django.core.context_processors.csrf(request))
        return django.shortcuts.render_to_response('pets/pet_insert.html', context)

    def post(self, request, *args, **kwargs):
        """ insert pet """
        pet_form = pet.forms.PetForm(request.POST)
        # get all pet videos from a json encoded string
        pet_videos = json.loads(request.POST['videos'])
        if pet_form.is_valid():
            print("is valid")
            new_pet_form = pet_form.save(commit=False)
            new_pet_form.organization = request.user
            new_pet_form.save()
            # save pet video
            for pet_video in pet_videos:
                pet_video_form = pet.forms.PetVideoForm(pet_video)
                print(pet_video_form)
                if pet_video_form.is_valid():
                    instance = pet_video_form.save(commit=False)
                    print("instance:", instance)
                    
                    print(instance.created_by_id)
                    if instance.created_by_id == None:
                        instance.created_by_id = request.user.id
                    if instance.pet_id == None:
                        instance.pet = new_pet_form
                        
                    # replacement for ordering as default 1
                    if instance.ordering is None:
                        instance.ordering = 1
                    instance.save()
                    print("instance in saved")
                else:
                    for error in pet_video_form.errors.items:
                        django.contrib.messages.error(request, error)
                    print(django.contrib.messages)
            return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:list'))
        else:
            print("not valid")
            for error in pet_form.errors:
                print(type(error))
                django.contrib.messages.error(request, error)
            # return django.shortcuts.render_to_response('pets/pet_insert.html', request)
        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:insert'))

class PetEditView(django.views.generic.UpdateView):
    # form_class = pet.forms.PetForm()
    # Below is generic view
    # model = pet.models.Pet
    template_name = "pets/pet_edit.html"
    success_url = django.core.urlresolvers.reverse_lazy('pet:list')
    
    def get(self, request, *args, **kwargs):
        pet_object = pet.models.Pet.objects.get(id = self.kwargs['pk'])
        pet_form = pet.forms.PetForm(instance=pet_object)
        pet_form.id = self.kwargs['pk']
        pet_videos = list(pet_object.videos.all())
        """pet_video_forms = []
        for pet_video in pet_videos:
            pet_video_forms.append(pet.forms.PetVideoForm(instance=pet_video))"""
        pet_videos = map(lambda x:x.toDict(), list(pet_videos))
        context = {'pet_form': pet_form, 'pet_videos':json.dumps(pet_videos)}
        context.update(django.core.context_processors.csrf(request))
        return django.shortcuts.render_to_response(self.template_name, context )
    
    def post(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        pet_object = django.shortcuts.get_object_or_404(pet.models.Pet, pk=object_id)
        pet_videos = json.loads(request.POST['videos'])
        pet_form = pet.forms.PetForm(data=request.POST, instance=pet_object)
        # check pet form is valid
        if pet_form.is_valid():
            print("is valid")
            new_pet_form = pet_form.save(commit=False)
            # get organization detail from login user
            new_pet_form.organization = request.user
            new_pet_form.save()
            # get all existing video
            pet_videos_ids = [x['video_id'] for x in pet_videos if 'video_id' in x]
            # get all new videos
            pet_videos_without_ids = [x for x in pet_videos if 'video_id' not in x]
            print(pet_videos_ids, pet_videos_without_ids)
            # delete removed videos
            try:
                pet.models.PetVideo.objects.exclude(pk__in=pet_videos_ids).filter(pet=pet_object).delete()
            except django.db.DatabaseError:
                print("Error in Pet Videos deletion")
            
            # insert each of the new pet videos
            for pet_video in pet_videos_without_ids:
                # pet_video_object = django.shortcuts.get_object_or_404(pet_video)
                pet_video_form = pet.forms.PetVideoForm(pet_video)
                print(pet_video_form)
                if pet_video_form.is_valid():
                    instance = pet_video_form.save(commit=False)
                    print("instance:", instance)
                    print(instance.created_by_id)
                    if instance.created_by_id == None:
                        instance.created_by_id = request.user.id
                    if instance.pet_id == None:
                        instance.pet = new_pet_form
                    # replacement for ordering as default 1
                    if instance.ordering is None:
                        instance.ordering = 1
                    instance.save()
                    print("instance in saved")
                else:
                    for error in pet_video_form.errors.items:
                        django.contrib.messages.error(request, error)
                    print(django.contrib.messages)
            return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:list'))
        else:
            print("not valid")
            for error in pet_form.errors:
                print(type(error))
                django.contrib.messages.error(request, error)
            # return django.shortcuts.render_to_response('pets/pet_insert.html', request)
        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:edit', kwargs={'pk':object_id}))

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

class PetView(assistedjson.views.JsonView):
    def get(self, request, *args, **kwargs):
        return django.shortcuts.render_to_response('pets/pet.html')
    
        
