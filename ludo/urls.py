from django.urls import path
from . import views

app_name = 'ludo'

urlpatterns = [
	path('', views.index, name='page'),
	path('game/', views.index, name='ludo'), 
	path("game/<str:room_code>/", views.game, name='lobby'),
]