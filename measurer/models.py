from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Material(models.Model):
	material_name = models.CharField(max_length=50)
	material_density = models.FloatField()
	created_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.material_name

class Shape(models.Model):
	shape_name = models.CharField(max_length=50)
	shape_realname = models.CharField(max_length=50)
	created_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s (%s)' % (self.shape_realname, self.shape_name)