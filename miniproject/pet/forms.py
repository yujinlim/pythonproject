import django.forms
import pet.models
import pet.fields

class PetForm(django.forms.ModelForm):
	date_of_birth = django.forms.DateField()
	# description = django.forms.CharField(widget=django.forms.widgets.TextInput)
	"""def __init__(self, *args, **kwargs):
		super(PetForm, self).__init__(*args, **kwargs)
		races = [(x.pk, x.name) for x in list(pet.models.Race.objects.filter(species_id = self.instance.species_id))]
		self.fields['race'] = django.forms.ChoiceField(choices = races, required=False)
		print(args, kwargs)"""

	"""def clean_race(self):
		print(self.data)
		species = self.data["species"][0]
		try:
			race = self.data["race"][0]
		except KeyError:
			return None
		else:
			if race == "":
				return None
		try:
			race = pet.models.Race.objects.get(pk=race, species_id=species)
		except pet.models.Race.DoesNotExist:
			raise django.forms.ValidationError("Race and species do not match")
		else:
			return race"""
		
	
	class Meta:
		model = pet.models.Pet

		
class PetVideoForm(django.forms.ModelForm):
	video_link = django.forms.CharField(widget=django.forms.widgets.TextInput)
	
	class Meta:
		model = pet.models.PetVideo
		exclude = ('pet', 'created_by', 'created_date')
	
	

#PetVideoFormSet = django.forms.models.inlineformset_factory(pet.models.Pet, pet.models.PetVideo)
