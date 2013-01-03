# Create your views here.
import django.views.generic
import django.shortcuts
import pet.models
import datetime
import django.db

# List of all pets
class PetListView (django.views.generic.View) :
	def get(self, request, *args):
		name = request.session.get('hello', 'nothing')
		dogs  = pet.models.Pet.objects.filter(name__istartswith='b')[:5]
		print dogs[0]
		print django.db.connection.queries
		return django.shortcuts.render_to_response("pets/base.html", {'now':datetime.datetime.now(), 'user': dogs[0] })

# Get single pet
class SinglePetView (django.views.generic.View) :
	def get(self, request, *args, **kwargs):
		
		
