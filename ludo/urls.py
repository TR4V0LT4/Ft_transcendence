from django.urls import path
from . import views
from ludo.consumers import Fconsumer

app_name = 'ludo'

urlpatterns = [
	path('', views.index, name='page'),
	 path('lobby/<room_code>/', views.lobby, name='lobby'),
	 path('game/', views.game, name='ludo'),
	 
]