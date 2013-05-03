import django.forms
import pet.models
import django.contrib.auth.models

class AppointmentForm(django.forms.ModelForm):
	# date_of_birth = django.forms.DateField()
	# description = django.forms.CharField(widget=django.forms.widgets.TextInput)
	class Meta:
		model = pet.models.Appointment
		exclude = ('pet')
		