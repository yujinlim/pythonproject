import django.db.models
import django.contrib.auth.models

# Create your models here.

class Species(django.db.models.Model):
	name = django.db.models.CharField(max_length = 255)
	
	def __unicode__(self):
		return self.name

class Race(django.db.models.Model):
	name = django.db.models.CharField(max_length = 255)
	species = django.db.models.ForeignKey(Species, related_name="races")
	
	def __unicode__(self):
		return self.name

class Pet(django.db.models.Model):
	name = django.db.models.CharField(max_length = 255)
	date_of_birth = django.db.models.DateField()
	description = django.db.models.TextField()
	race = django.db.models.ForeignKey(Race, null = True, blank = True)
	species = django.db.models.ForeignKey(Species, related_name="pets")
	created_datetime = django.db.models.DateTimeField(auto_now=True)
	available_until = django.db.models.DateField(blank=True, null=True)
	organization = django.db.models.ForeignKey(django.contrib.auth.models.User)
	
	
class PetVideo(django.db.models.Model):
	video_link = django.db.models.TextField()
	ordering = django.db.models.IntegerField()
	pet = django.db.models.ForeignKey(Pet, related_name="videos")
 
