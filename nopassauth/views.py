import secrets
import requests
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from oauthlib.oauth2 import WebApplicationClient
from django.shortcuts import render

# Create your views here.

def auth_login(request):
	client_id = settings.OAUTH42_CLIENT_ID
	client = WebApplicationClient(client_id)
	request.session['state'] = secrets.token_urlsafe(16)
	authorization_url = 'https://api.intra.42.fr/oauth/authorize'

	url = client.prepare_request_uri(
		authorization_url,
		redirect_uri = settings.OAUTH42_CALLBACK_URL,
		scope = ['public'], 
		state = request.session['state'],
		allow_signup = 'false'
	)

	return HttpResponseRedirect(url)

class CallbackView(TemplateView):
	def get(self, request, *args, **kwargs):
		data = self.request.GET
		code = data['code']
		# state = data['state']
		# print("code=%s, state=%s" %(code))
		# if self.request.session['state'] != state:
		# 	messages.add_message(self.request, messages.ERROR, 'Invalid state')
		# 	return HttpResponseRedirect(reverse('github:welcome'))
		# else:
			# del self.request.session['state']
		token_url = 'https://api.intra.42.fr/oauth/token'
		client_id = settings.OAUTH42_CLIENT_ID
		client_secret = settings.OAUTH42_SECRET
		client = WebApplicationClient(client_id)
		data = client.prepare_request_body(	
			code = code,
			redirect_uri = settings.OAUTH42_CALLBACK_URL,
			client_id = client_id,
			client_secret = client_secret,
		)
		response = requests.post(token_url, data=data)
		client.parse_request_body_response(response.text)
		header = {'Authorization': 'Bearer {}'.format(client.token['access_token'])}
		print (header)
		response = requests.get('https://api.intra.42.fr/v2/me', headers=header)
		json_dict = response.json()
		print (response.text)
		self.request.session['profile'] = json_dict
		try:
			user = User.objects.get(username=json_dict['login'])
			messages.add_message(self.request, messages.DEBUG, "User %s already exists, Authenticated? %s" %(user.username, user.is_authenticated))	
			login(self.request, user)
		except:
			user = User.objects.create_user(json_dict['login'], json_dict['email'])
			messages.add_message(self.request, messages.DEBUG, "User %s is created, Authenticated %s?" %(user.username, user.is_authenticated))
			login(self.request, user)
		return HttpResponseRedirect(reverse('nopassauth:welcome'))
	
class WelcomeView(TemplateView):
  template_name = 'welcome.html'

class PageView(TemplateView):
  template_name = 'page.html'

class HomeView(TemplateView):
  template_name = 'home.html'

def logout_request(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, "You have been logged out")
	return render(request, 'home.html')