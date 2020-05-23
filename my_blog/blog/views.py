from django.shortcuts import render
from .models import Post
from django.views import generic

class HomeView(generic.ListView):
	template_name = "blog/home.html"
	context_object_name = "latest_post"
	def get_queryset(self):
		return Post.objects.order_by("-pub_date")[:10]

class DetailView(generic.DetailView):
	model = Post
	template_name = 'blog/detail.html'
