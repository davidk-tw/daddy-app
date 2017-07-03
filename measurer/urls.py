from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<shape>\w+)/$', views.scale, name='scale'),
	url(r'^(?P<shape>\w+)/result/$', views.measure, name='measure'),
	url(r'^add/material/$', views.add_material, name='add_material'),
	url(r'^show/materials/$', views.display_material, name='display_material')
]
