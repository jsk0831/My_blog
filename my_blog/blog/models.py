import datetime
from django.db import models
from django.utils import timezone

class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	pub_date = models.DateField( auto_now = True )
	category = models.CharField(max_length = 50)
	views = models.IntegerField(default = 0)
	comments = models.IntegerField(default = 0)

	def __str__(self):
		return self.title
	def get_pub_date(self):
		return "{}-{}-{} {}:{}".format( self.pub_date.year, self.pub_date.month, self.pub_date.day, self.pub_date.hour, self.pub_date.minute)


class Comment(models.Model):
	post = models.ForeignKey( Post, on_delete = models.CASCADE )
	content = models.CharField( max_length = 5000 )
	pub_date = models.DateField( auto_now = True )
	author = models.CharField( max_length = 20 )