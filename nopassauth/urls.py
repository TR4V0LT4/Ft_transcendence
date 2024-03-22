from django.urls import path
from . import views
from .views import CallbackView, WelcomeView, HomeView, PageView

app_name = 'nopassauth'

urlpatterns = [
  path('', HomeView.as_view(), name='home'),
  path('login/', views.auth_login, name='login'),  
  path('callback/', CallbackView.as_view(), name='callback'), 
  path('welcome/', WelcomeView.as_view(), name='welcome'),    		
  path('page/', PageView.as_view(), name='page'),
  path('logout/', views.logout_request, name='logout'),
]