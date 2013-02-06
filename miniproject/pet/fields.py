import django.forms

class RaceField(django.forms.ChoiceField):
	def __init__(self, **kwargs):
		print(self.instance)
		return super(RaceField, self).__init__(kwargs)
