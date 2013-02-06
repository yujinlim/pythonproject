# Create your views here.
import django.views.generic
import django.shortcuts
import datetime
import django.db
import assistedjson.views
import django.template
import django.core.urlresolvers
import django.contrib.auth
import django.contrib.messages
from django.utils.translation import ugettext as _
import django.http


class LoginView(django.views.generic.View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('pet:list'))
		return django.shortcuts.render_to_response("backend/login.html", context_instance=django.template.RequestContext(request))
	
	def post(self, request, *args, **kwargs):
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		print(username, password)
		user = django.contrib.auth.authenticate(username= username, password=password)
		if user is None:
			# Translators: Failed to login
			django.contrib.messages.error(request, _('There is no user'))
			return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse('backend:adminlogin'))
		else:
			django.contrib.auth.login(request, user)
			return django.http.HttpResponseRedirect(request.GET.get('next', django.core.urlresolvers.reverse('pet:list')))


		
	
