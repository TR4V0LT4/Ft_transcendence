from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=100)
	email = models.EmailField()
	# password = models.CharField(max_length=100)
	image_url = models.URLField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def create_user(self, username, email, image_url):
		user = User(username=username, email=email, image_url=image_url)
		user.save()
		return user
	
	def __str__(self):
		return self.username