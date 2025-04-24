from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	login = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=200, default='')
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
	matches = models.ManyToManyField('Match', related_name='players', blank=True)
	stats = models.OneToOneField('Stats', on_delete=models.CASCADE, null=True, blank=True)
	
	def __str__(self):
		return self.username
	
class Match(models.Model):
	date = models.DateField()
	user1 = models.CharField(max_length=100)
	user2 = models.CharField(max_length=100)
	winner = models.CharField(max_length=100)
	result_user1 = models.IntegerField()
	result_user2 = models.IntegerField()
	  
	def __str__(self):
		return self.user1 + ' vs ' + self.user2
	
class Stats(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_stats')
	wins = models.IntegerField(default=0)
	games_played = models.IntegerField(default=0)
	winrate = models.FloatField(default=0)
	score = models.IntegerField(default=1000)
	highest_score = models.IntegerField(default=0)

	def get_winrate(self):
		if self.games_played == 0:
			return 0
		return self.wins / self.games_played * 100
	
	def get_highest_score(self):
		if self.score > self.highest_score:
			self.highest_score = self.score
		return self.highest_score
	
	def __str__(self):
		return self.user.username + ' stats'