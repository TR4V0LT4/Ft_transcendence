from django.urls import re_path, path
from . import views

app_name = 'pong'

urlpatterns = [
	re_path(r'^pong', views.redirect, name='pong'),
]
