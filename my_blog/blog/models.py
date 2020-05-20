import datetime
from django.db import models
from django.utils import timezone

class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	pub_date = models.DateTimeField(default = timezone.now() )
	category = models.CharField(max_length = 50)
	views = models.IntegerField(default = 0)
	comment = models.IntegerField(default = 0)
	def __str__(self):
		return self.title
	def str_pub_date(self):
		return "{}-{}-{} {}:{}".format( self.pub_date.year, self.pub_date.month, self.pub_date.day, self.pub_date.hour, self.pub_date.minute)