import django.db.models
import django.contrib.auth.models
import assistedjson.models

# Create your models here.

class Species(assistedjson.models.SerializableModel):
	name = django.db.models.CharField(max_length = 255)
	
	def __unicode__(self):
		return self.name

class Race(assistedjson.models.SerializableModel):
	name = django.db.models.CharField(max_length = 255)
	species = django.db.models.ForeignKey(Species, related_name="races")
	
	def __unicode__(self):
		return self.name

class Pet(assistedjson.models.SerializableModel):
	name = django.db.models.CharField(max_length = 255)
	date_of_birth = django.db.models.DateField()
	description = django.db.models.TextField()
	species = django.db.models.ForeignKey(Species, related_name="pets")
	race = django.db.models.ForeignKey(Race, null = True, blank = True)
	created_datetime = django.db.models.DateTimeField(auto_now=True)
	available_until = django.db.models.DateField(blank=True, null=True)
	organization = django.db.models.ForeignKey(django.contrib.auth.models.User)
	
	
class PetVideo(assistedjson.models.SerializableModel):
	title = django.db.models.TextField()
	video_link = django.db.models.TextField()
	ordering = django.db.models.IntegerField()
	created_by = django.db.models.ForeignKey(django.contrib.auth.models.User, related_name="videos")
	created_date = django.db.models.DateTimeField(auto_now=True)
	published = django.db.models.BooleanField(default=True)
	pet = django.db.models.ForeignKey(Pet, related_name="videos")

class Donation(assistedjson.models.SerializableModel):
	name = django.db.models.TextField()
	email = django.db.models.EmailField(max_length=254)
	donation_date = django.db.models.DateTimeField(auto_now=True)
	pet = django.db.models.ForeignKey(Pet, related_name="donation")
	amount = django.db.models.DecimalField(max_digits=19, decimal_places=2)

class PetVideoNext(assistedjson.models.SerializableModel):
	video = django.db.models.ForeignKey(PetVideo, related_name="video counts")
	ip = django.db.models.CharField(max_length=255)
	next_date = django.db.models.DateTimeField(auto_now=True)
	
class Organization(assistedjson.models.SerializableModel):
	name = django.db.models.CharField(max_length=255)
	address = django.db.models.TextField()
	email = django.db.models.EmailField()
	contact_number = django.db.models.CharField(max_length=255, null=True, blank=True)
	created_datetime = django.db.models.DateTimeField(auto_now=True)
	youtube_channel = django.db.models.CharField(max_length=255, null=True, blank=True)
	user = django.db.models.OneToOneField(django.contrib.auth.models.User, primary_key=True)
	
class Appointment(assistedjson.models.SerializableModel):
	name = django.db.models.CharField(max_length=255)
	email = django.db.models.EmailField()
	contact_number = django.db.models.CharField(max_length=255)
	created_datetime = django.db.models.DateTimeField(auto_now=True)
	appointment_datetime = django.db.models.DateTimeField()
	appointment_time = django.db.models.DateTimeField()
	pet = django.db.models.ForeignKey(Pet, related_name="appointments")

class AppointmentConfirmation(assistedjson.models.SerializableModel):
	APPOINTMENT_STATUS = (
						(0, 'in progress'),
						(1,'adopted'), 
						(2, 'rejected'),
						(3, 'pending'),
						)
	
	confirmed_date = django.db.models.DateTimeField()
	status = django.db.models.CharField(max_length=255, choices=APPOINTMENT_STATUS, default=0)
	appointment = django.db.models.OneToOneField(Appointment, primary_key=True, related_name="appointment_confirm_status")
