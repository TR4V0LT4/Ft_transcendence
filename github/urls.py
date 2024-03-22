from django.urls import path
from . import views
from .views import CallbackView, WelcomeView, HomeView, PageView

app_name = 'github'

urlpatterns = [
	path('git/', HomeView.as_view(), name='home'),
  path('git/login/', views.github_login, name='login'),  
  path('git/callback/', CallbackView.as_view(), name='callback'), 
  path('git/welcome/', WelcomeView.as_view(), name='welcome'),    		
  path('git/page/', PageView.as_view(), name='page'),
  path('git/logout/', views.logout_request, name='logout'),
]