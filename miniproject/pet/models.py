import django.db.models

# Create your models here.

class Species(django.db.models.Model):
	name = django.db.models.CharField(max_length = 255)

class Race(django.db.models.Model):
	name = django.db.models.CharField(max_length = 255)
	species = django.db.models.ForeignKey(Species)

class Pet(django.db.models.Model):
	name = django.db.models.CharField(max_length = 255)
	date_of_birth = django.db.models.DateField()
	description = django.db.models.TextField()
	race = django.db.models.ForeignKey(Race, null = True, blank = True)
	species = django.db.models.ForeignKey(Species)

