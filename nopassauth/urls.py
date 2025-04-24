from django.urls import path
from . import views
from .views import CallbackView, WelcomeView, HomeView, ProfileView, LoginView

app_name = 'nopassauth'

urlpatterns = [
  path('', HomeView.as_view(), name='home'),
  path('42login/', views.auth_login, name='42login'),  
  path('callback/', CallbackView.as_view(), name='callback'), 
  path('welcome/', WelcomeView.as_view(), name='welcome'),
  path('logout/', views.logout_request, name='logout'),
  path('profile/', ProfileView.as_view(), name='profile'),
  path('login/', LoginView.as_view(), name="login"),
  path('settings/', views.profile_settings, name='settings'),
  # path('set_pass/', views.change_password, name='set_pass'),
]