import secrets
import requests
import os
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import View
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from oauthlib.oauth2 import WebApplicationClient
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Stats, Match
from .forms import SetPasswordForm
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed



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

class LoginView(TemplateView):
	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')

		print(username, password)
		
		try:
			#find user bu username
			user_profile = UserProfile.objects.get(login=username)
		except UserProfile.DoesNotExist:
			messages.error(request, 'User Not Found')
			return HttpResponseRedirect(reverse('nopassauth:home'))
		
		# Check if password matches the hashed password in the database
		if check_password(password, user_profile.password):
		# Password matches, log in the user
			login(request, user_profile.user)
			return HttpResponseRedirect(reverse('nopassauth:welcome'))
		else:
			messages.error(request, 'Incorrect password')
			return HttpResponseRedirect(reverse('nopassauth:home'))

		

class CallbackView(TemplateView):
	template_name = "set_password.html"
	def get(self, request, *args, **kwargs):
		# Retrieve the OAuth code from the GET parameters
		data = self.request.GET
		code = data['code']
		# Exchange the code for an access token
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
		# Retrieve user information from the OAuth provider's API
		response = requests.get('https://api.intra.42.fr/v2/me', headers=header)
		json_dict = response.json()
		# Store user profile data in the session
		self.request.session['profile'] = json_dict

		try:
			# Check if the user already exists in the database
			user = User.objects.get(username=json_dict['login'])
			messages.add_message(self.request, messages.DEBUG, "User %s already exists, Authenticated? %s" %(user.username, user.is_authenticated))	
		except:
			# If the user doesn't exist, create a new user
			user = User.objects.create_user(json_dict['login'], json_dict['email'])
			messages.add_message(self.request, messages.DEBUG, "User %s is created, Authenticated %s?" %(user.username, user.is_authenticated))
		
		@receiver(post_save, sender=User)
		def create_user_profile(sender, instance, created, **kwargs):
			if created:
				UserProfile.objects.create(user=instance)
        		# Create associated Stats instance
				Stats.objects.create(user=user_profile)
		
		@receiver(post_save, sender=UserProfile)
		def create_stats(sender, instance, created, **kwargs):
			if created:
				Stats.objects.create(user=instance)

		# @receiver(post_save, sender=UserProfile)
		# def create_stats(sender, instance, created, **kwargs):
		# 	if created:
		# 		Stats.objects.create(user=instance.user)
		# # Create or update UserProfile instance and save additional data
		user_profile, create = UserProfile.objects.get_or_create(user=user)
		try:
			stats_instance = Stats.objects.get(user_id=user_profile.id)
		except Stats.MultipleObjectsReturned:
			stats_instance = Stats.objects.filter(user_id=user_profile.id).first()
		except Stats.DoesNotExist:
			stats_instance = Stats.objects.create(user_id=user_profile.id)
		user_profile.stats = stats_instance
		user_profile.login = json_dict['login']
		user_profile.username = json_dict['login']
		user_profile.name = json_dict['usual_full_name']
		# # Stats.objects.create(user=user.userprofile)
		

		# Extract the image URL from the JSON response
		image_url = json_dict.get('image',{}).get('link')

		# Download and save the image to UserProfile model
		if image_url:
			try:
				response = requests.get(image_url)
				if response.status_code == 200:
					# save the image to userprofile
					if not user_profile.image:
						user_profile.image.save('profile.jpg', ContentFile(response.content), save=True)
				else:
					messages.add_message(self.request, messages.ERROR, f"Failed to download image from {image_url}")
			except Exception as e:
					messages.add_message(self.request, messages.ERROR, f"Error downloading image: {e}")

		# log in the user
		login(self.request, user)
		# Log out the user
		
		#Set Password Logic
		user_profile = UserProfile.objects.get(user=user)
		if not user_profile.password:
			# render the set password form
			form = SetPasswordForm()
			return self.render_to_response({'form': form})
		else:
			return HttpResponseRedirect(reverse('nopassauth:welcome'))

	def post(self, request, *args, **kwargs):
		#Handle form submission to set the password
		form = SetPasswordForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			#check if the password is strong
			if not is_strong_password(password):
				form.add_error('password', 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
				return self.render_to_response({'form' : form})
			#hash password
			hashed_password = make_password(password)
			#update the user's password
			user_profile = UserProfile.objects.get(user=request.user)
			user_profile.password = hashed_password
			user_profile.save()
			#redirect to the welcome page
			return HttpResponseRedirect(reverse('nopassauth:welcome'))
		else:
			return self.render_to_response({'form': form})
		
	# def post(self, request, *args, **kwargs):
	# # Handle form submission to set the password
	# 	form = SetPasswordForm(request.POST)
	# 	if form.is_valid():
	# 		password = form.cleaned_data['password']
	# 		# Check if the password is strong
	# 		if not is_strong_password(password):
	# 			form.add_error('password', 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
	# 			return self.render_to_response({'form': form})
	# 		# Hash password
	# 		hashed_password = make_password(password)
	# 		# Update the user's password
	# 		user_profile = UserProfile.objects.get(user=request.user)
	# 		user_profile.password = hashed_password
	# 		user_profile.save()
	# 	# Redirect to the welcome page
	# 		return HttpResponseRedirect(reverse('nopassauth:welcome'))
	# 	else:
	# 	# Render custom template 'set_password.html' with form
	# 		return render(request, 'password.html', {'form': form})


class WelcomeView(LoginRequiredMixin, TemplateView):
  template_name = 'menu_alt.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    user_profile = UserProfile.objects.get(user=user)
    context['profile'] = user_profile
    return context
	

class HomeView(TemplateView):
  template_name = 'login_new.html'

  def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('nopassauth:welcome')
        else:
            return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'profile_alt.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		user_profile = UserProfile.objects.get(user=user)
		context['profile'] = user_profile
		return context	

def logout_request(request):
	logout(request)
	return render(request, 'login_new.html')

# Example: Password must be at least 8 characters long and contain at least one uppercase letter,
# one lowercase letter, one digit, and one special character
def is_strong_password(password):
	if len(password) < 8:
		return False
	if not any(char.isupper() for char in password):
		return False
	if not any(char.islower() for char in password):
		return False
	if not any(char in '!@#$%^&*()_+[]{}|;:,.<>?/~`' for char in password):
		return False
	return True

# views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def profile_settings(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        # Update username
        user_profile.username = request.POST.get('username')
        user_profile.save()

        # Update profile image
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
        
        # Change password
        # password = request.POST.get('password')
        # confirm_password = request.POST.get('confirm_password')
        # if password and password == confirm_password:
        #     request.user.set_password(password)
        #     request.user.save()
        #     update_session_auth_hash(request, request.user)  # Update session with new password
        #     messages.success(request, 'Password changed successfully.')
        # elif password and password != confirm_password:
        #     messages.error(request, 'Passwords do not match.')
    
    return render(request, 'settings.html', {'user_profile': user_profile})
