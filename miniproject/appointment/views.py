import django.views.generic
import django.shortcuts
import pet.models
import datetime
import django.db
import assistedjson.views
import paginatedview.views
import django.template
import django.core.urlresolvers
import appointment.forms
import organization.forms
import json
import django.core
import django.core.serializers
import django.contrib.messages
import django.http
import django.core.context_processors


class AppointmentListView(assistedjson.views.JsonView):
    def get(self, request, *args, **kwargs):
        entries_url = django.core.urlresolvers.reverse('appointment:entries')
        context = {'page_title':'List Of Organizations', 'entries_url':entries_url}
        return django.shortcuts.render_to_response("backend/base_list.html", context)

# get all appointments
class AppointmentEntriesView(assistedjson.views.LoginRequiredJsonView, paginatedview.views.PaginatedView):
    def get(self, request, *args, **kwargs):
        context = self.prepare_paginated_context(request)
        self._response.debug('done')
        self._response.html(django.template.loader.render_to_string("appointment/appointment_entries.html", context))
        return self.respond()
        #django.shortcuts.render_to_response("pets/entries_list.html", context)

    def get_queryset(self, request):
        qs = pet.models.Appointment.objects.all()
        if request.user.is_authenticated() and not request.user.is_superuser:
            qs = qs.filter(author = request.user)
        return qs
    
    def per_page(self):
        return 5
    
# Update Appointment Status
class AppointmentUpdateView(django.views.generic.View):
    # success_url = django.core.urlresolvers.reverse_lazy('pet:list')
    
    def get(self, request, *args, **kwargs):
        """ get form for insert pet """
        organization_form = organization.forms.OrganizationForm()
        user_form = organization.forms.UserForm()
        # print(pet_form, pet_video_form)
        context = {'organization_form': organization_form,'user_form': user_form}
        context.update(django.core.context_processors.csrf(request))
        return django.shortcuts.render_to_response('organization/organization_insert.html', context)

    def post(self, request, *args, **kwargs):
        pass
        """ insert user """
        user_form = organization.forms.UserForm(request.POST)
        if user_form.is_valid():
            print("is valid")
            user_object = user_form.save()
            organization_form = organization.forms.OrganizationForm(request.POST)
            #print(organization_form)
            if organization_form.is_valid():
                instance = organization_form.save(commit=False)
                print(instance, instance.name)
                if instance.user_id == None:
                    instance.user = user_object
                if instance.email == "":
                    instance.email = user_object.email
                instance.save()
                print("instance in saved")
                return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('organization:list'))
            else:
                for error in organization_form.errors:
                    print(error)
                    django.contrib.messages.error(request, error)
                print("error in saving organization")
        else:
            print("not valid")
            for error in user_form.errors:
                print(error)
                django.contrib.messages.error(request, error)
        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('organization:insert'))

class AppointmentInsertView(django.views.generic.CreateView):
    model = pet.models.Appointment
    form_class = appointment.forms.AppointmentForm
    template_name = "appointment/appointment_insert.html"
    
        
