from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
	path('', include('github.urls')),
	path('', include('nopassauth.urls')),
	path('admin/', admin.site.urls),
	path('ludo/', include('ludo.urls')), 
]
