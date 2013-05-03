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
import random


class RandomApi(assistedjson.views.JsonView):
    def get(self, request, *args, **kwargs):
        """get request for a random video"""
        # grab videos from the sessions
        watched_videos = request.session.get("watched_videos", [])
        video = self.get_random_video(watched_videos)
        if video is None:
            watched_videos = []
            video = self.get_random_video(watched_videos)
            
        watched_videos.append(video.pk)
        request.session["watched_videos"] = watched_videos
        
        # store current video id into session
        request.session["current_video"] = video.pk
        pet = video.pet.toDict()
        pet["next_count"] = self.get_next_count(pet["id"])
        as_Dict = video.toDict()
        as_Dict["pet"] = pet
        # parse video as json response
        self._response.data(key="video", value=as_Dict)
        self._response.debug('done')
        return self.respond()
    
    def get_random_video(self, watched):
        """grab a random video"""
        videos_count = pet.models.PetVideo.objects.exclude(pk__in=watched).count()

        if videos_count > 1:
            row_number = random.randrange(0, videos_count)
        elif videos_count == 1:
            row_number = 0
        else:
            return None
        
        qs = pet.models.PetVideo.objects.exclude(pk__in=watched).all()[row_number: row_number + 1][0]
        return qs
    
    def get_next_count(self, pet_id):
        """get count for nexted pet"""
        next_count = pet.models.PetVideoNext.objects.filter(video__in=pet.models.PetVideo.objects.filter(pet__pk=pet_id)).count()
        return next_count
    
class NextApi(RandomApi):
    """video been next"""
    def get(self, request, *args, **kwargs):
        print("getting it done")
        current_video_id = request.session["current_video"]
        ip = self.get_user_ip(request)
        self.store_next_video(video_id=current_video_id, ip_address=ip)
        
        # return get request for a random video
        return super(NextApi, self).get(request, *args, **kwargs)
        
    
    def store_next_video(self, **kwargs):
        try:
            pet.models.PetVideoNext.objects.create(video_id = kwargs.get("video_id"), ip = kwargs.get("ip_address"))
            print("done")
        except:
            print("fail")
            return False
        
    def get_user_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class DetailApi(assistedjson.views.JsonView):
    """get request for pet details"""
    
    def get(self, request, *args, **kwargs):
        # grab current video id
        video_id = request.session["current_video"]
        
        # grab pet details 
        pet = self.get_pet_details(video_id)
        pet_species_name = pet.species.name
        try:
            pet_race_name = pet.race.name
        except:
            pet_race_name = ""
        # grab videos for this pet
        pet_videos = pet.videos.all()
        pet_organization = self.get_organization(pet.organization_id)
        # parse to dict for every video
        pet_videos = map(lambda x:x.toDict(), list(pet_videos))
        # insert into a dictionary
        as_Dict = pet.toDict()
        as_Dict["videos"] = pet_videos
        as_Dict["organization"] = pet_organization.toDict()
        as_Dict["species_name"] = pet_species_name
        as_Dict["race_name"] = pet_race_name
        self._response.data(key="pet", value=as_Dict)
        self._response.debug("done")
        return self.respond()
    
    def get_pet_details(self, video_id):
        # grab pet details
        the_pet = pet.models.Pet.objects.get(videos__pk=video_id)
        return the_pet
    
    def get_organization(self, user_id):
        organization_details = pet.models.Organization.objects.get(user_id=user_id)
        return organization_details
            
class AppointmentApi(DetailApi):
    def post(self, request, *args, **kwargs):
        # grab all details on post
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        contact_number = request.POST.get('contact_number', None)
        appointment_date =  request.POST.get('date', None)
        video_id = request.session["current_video"]
        pet =  self.get_pet_details(video_id)
        if appointment_date is not None:
            if type(appointment_date) != datetime.datetime.date():
                self._response.data(key="date_error", value="Date format error") 
        appointment_time = request.POST.get('time', None)
        if appointment_time is not None:
            if type(appointment_time) != datetime.datetime.time():
                self._response.data(key="time_error", value="Time format error")
        if name is not None and email is not None and contact_number is not None and appointment_date is not None and appointment_time is not None:
            appointment_result = self.set_appointment(name, email, contact_number, appointment_date, appointment_time, pet)
            self._response.data(key="appointment_result", value=str(appointment_result))
            self._response.debug("done")
        else:
            self._response.debug("fail")
            self._response.data(key="appointment_result", value="fail")
        return self.respond()
    
    def get(self, request, *args, **kwargs):
        # grab current video id
        video_id = request.session["current_video"]
        
        # grab pet details 
        pet = self.get_pet_details(video_id)
        
        # grab videos for this pet
        # pet_videos = pet.videos.all()
        
        #grab all appointments for this pet
        pet_appointments = pet.appointments.all()
        # pet_organization = self.get_organization(pet.organization_id)
        
        # parse to dict for every video
        # pet_videos = map(lambda x:x.toDict(), list(pet_videos))
        
        pet_appointments = map(lambda x:x.toDict(), list(pet_appointments))
        # insert into a dictionary
        as_Dict = pet_appointments
        # as_Dict["organization"] = pet_organization.toDict()
        
        # as_Dict["appointments"] = pet_appointments
        self._response.data(key="appointments", value=as_Dict)
        self._response.debug("done")
        self._response.message("This returns current pet's appointments list")
        return self.respond()
    
    def set_appointment(self, name, email, contact_number, appointment_date, appointment_time, pet):
        try:
            pet.models.Appointment.objects.create(name=name, email=email, contact_number=contact_number, appointment_datetime = appointment_date, appointment_time = appointment_time, pet=pet)
        except:
            return False
        return True

class AppointmentConfirmationApi():
    pass


class DonationApi(assistedjson.views.JsonView):
    def post(self, request, *args, **kwargs):
        pass