from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
	path("", views.Home.as_view(), name = "home"),
	path("<int:pk>/", views.Detail.as_view(), name = "detail"),
	path("publish/", views.Publish.as_view(), name = 'publish' ),
]