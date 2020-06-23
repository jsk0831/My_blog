import datetime
from django.db import models
from django.utils import timezone

class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	pub_date = models.DateTimeField( auto_now_add = True )
	category = models.CharField(max_length = 50)
	views = models.IntegerField(default = 0)
	comments = models.IntegerField(default = 0)

	def __str__(self):
		return self.title
	def get_pub_date(self):
		return "{}-{}-{} {}:{}".format( self.pub_date.year, self.pub_date.month, self.pub_date.day, self.pub_date.hour, self.pub_date.minute)
	def plus_views(self):
		self.views += 1
	def update_comments( self, comments ):
		self.comments = comments
		self.save()


class Comment(models.Model):
	post = models.ForeignKey( Post, on_delete = models.CASCADE )
	content = models.CharField( max_length = 5000 )
	pub_date = models.DateTimeField( auto_now_add = True )
	like = models.IntegerField( default = 0 )
	user = models.ForeignKey( 'User', default = 1, on_delete = models.CASCADE )

	def get_pub_date(self):
		return "{}-{}-{} {}:{}".format( self.pub_date.year, self.pub_date.month, self.pub_date.day, self.pub_date.hour, self.pub_date.minute)
	def plus_like(self):
		self.like += 1
		self.save()

class User(models.Model):
	name = models.CharField( max_length = 20 )
	pw = models.CharField( max_length = 20 )
	address = models.ForeignKey( 'address', on_delete = models.DO_NOTHING )

class Address(models.Model):
	post = models.ForeignKey( Post, on_delete = models.CASCADE )
	ip = models.CharField( max_length = 20 )