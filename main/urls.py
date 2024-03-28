from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include('github.urls')),
	path('', include('nopassauth.urls')),
	path('admin/', admin.site.urls),
	path('ludo/', include('ludo.urls')), 
	path('', include('pong.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
