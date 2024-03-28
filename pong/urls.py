from django.urls import re_path
from . import views

app_name = 'pong'

urlpatterns = [
	re_path(r'^pong', views.redirect, {'var': 1234}, name='pong'),
]
