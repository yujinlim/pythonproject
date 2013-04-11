import django.forms
import pet.models
import django.contrib.auth.models

class OrganizationForm(django.forms.ModelForm):
	# date_of_birth = django.forms.DateField()
	# description = django.forms.CharField(widget=django.forms.widgets.TextInput)
	class Meta:
		model = pet.models.Organization
		exclude = ('user', 'email')

class UserForm(django.forms.ModelForm):
	 # video_link = django.forms.CharField(widget=django.forms.widgets.TextInput)
	
	class Meta:
		model = django.contrib.auth.models.User
		exclude = ('is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'user_permissions', 'groups')
	
	def clean_email(self):
		data = self.cleaned_data['email']
		print(data)
		if django.contrib.auth.models.User.objects.filter(email=data).exists():
			raise django.forms.ValidationError("This email already used")
		return data
	
	def clean_username(self):
		data = self.cleaned_data['username']
		print(data)
		if django.contrib.auth.models.User.objects.filter(username=data).exists():
			raise django.forms.ValidationError("This username already used")
		return data
		