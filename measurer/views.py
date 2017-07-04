# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Material, Shape

import math

# Create your views here.

def index(request):
	
	shapes = Shape.objects.all()

	return render(request, 'measurer/shape.html', {
		'shapes': shapes,
	})

def scale(request, shape):
	target = get_object_or_404(Shape, shape_name=shape)
	materials = Material.objects.all()

	need_to_scale = {
		'outer_radius': {
			'realname': '外徑',
			'list': ['tube']
		},
		'thickness': {
			'realname': '厚度',
			'list': ['tube', 'rectangular_tube', 'plate', 'angle', 'channel', 'beam', 'storage_tank_square']
		},
		'width': {
			'realname': '寬度',
			'list': ['plate', 'rectangular_tube', 'cuboid', 'storage_tank_square']
		},
		'length': {
			'realname': '長度',
			'list': ['tube', 'round_bar', 'plate', 'rectangular_tube', 'cuboid', 'hexagonal', 'octagonal', 'angle', 'storage_tank_square']
		},
		'height': {
			'realname': '高度',
			'list': ['rectangular_tube', 'cuboid', 'storage_tank_square']
		},
		'radius': {
			'realname': '半徑',
			'list': ['round_bar', ]
		},
		'diagonal': {
			'realname': '對角線長度',
			'list': ['hexagonal', 'octagonal']
		},
		'side_length_1': {
			'realname': '邊長',
			'list': ['angle']
		},
		'side_length_2': {
			'realname': '邊長',
			'list': ['angle']
		},
	}

	return render(request, 'measurer/scale.html', {
		'shape': target,
		'materials': materials,
		'scale_form': need_to_scale
	})

def measure(request, shape):
	shape = get_object_or_404(Shape, shape_name=shape)
	material = get_object_or_404(Material, pk=request.POST['select-material'])
	amount = int(request.POST['amount'])
	weight = 0.0
	spec = {}

	if shape.shape_name == 'tube':
		outer_radius = convert(request.POST['outer_radius-unit'], float(request.POST['outer_radius']))
		thickness = convert(request.POST['thickness-unit'], float(request.POST['thickness']))
		length = convert(request.POST['length-unit'], float(request.POST['length']))

		spec = {
			'外徑': outer_radius,
			'壁厚': thickness,
			'長度': length
		}

		weight = material.material_density * .001 * (outer_radius - thickness) * thickness * math.pi

	elif shape.shape_name == 'round_bar':
		radius = convert(request.POST['radius-unit'], float(request.POST['radius']))
		length = convert(request.POST['length-unit'], float(request.POST['length']))

		spec = {
			'半徑': radius,
			'長度': length
		}

		weight = material.material_density * .001 * pow(radius, 2) * length * math.pi

	elif shape.shape_name == 'plate':
		length = convert(request.POST['length-unit'], float(request.POST['length']))
		thickness = convert(request.POST['thickness-unit'], float(request.POST['thickness']))
		width = convert(request.POST['width-unit'], float(request.POST['width']))

		spec = {
			'長度': length,
			'厚度': thickness,
			'寬度': width
		}

		weight = material.material_density * .001 * length * width * thickness

	elif shape.shape_name == 'rectangular_tube':
		length = convert(request.POST['length-unit'], float(request.POST['length']))
		width = convert(request.POST['width-unit'], float(request.POST['width']))
		thickness = convert(request.POST['thickness-unit'], float(request.POST['thickness']))
		height = convert(request.POST['height-unit'], float(request.POST['height']))
		
		spec = {
			'長度': length,
			'寬度': width,
			'高度': height,
			'壁厚': thickness,
		}

		weight = material.material_density * .001 * (length + width) * 2 * height

	elif shape.shape_name == 'cuboid':
		length = convert(request.POST['length-unit'], float(request.POST['length']))
		width = convert(request.POST['width-unit'], float(request.POST['width']))
		height = convert(request.POST['height-unit'], float(request.POST['height']))
		
		spec = {
			'長度': length,
			'寬度': width,
			'高度': height,
		}

		weight = material.material_density * .001 * length * width * height

	elif shape.shape_name == 'hexagonal' or shape.shape_name == 'octagonal':
		constant = .866 if shape.shape_name == 'hexagonal' else .828
		diagonal = convert(request.POST['diagonal-unit'], float(request.POST['diagonal']))
		length = convert(request.POST['length-unit'], float(request.POST['length']))
		
		spec = {
			'長度': length,
			'對角線長度': diagonal
		}

		weight = material.material_density * .001 * pow(diagonal, 2) * length * constant

	elif shape.shape_name == 'angle':
		side_length_1 = convert(request.POST['side_length_1-unit'], float(request.POST['side_length_1']))
		side_length_2 = convert(request.POST['side_length_2-unit'], float(request.POST['side_length_2']))
		thickness = convert(request.POST['thickness-unit'], float(request.POST['thickness']))
		length = convert(request.POST['length-unit'], float(request.POST['length']))
		
		spec = {
			'邊長-1': side_length_1,
			'邊長-2': side_length_2,
			'厚度': thickness,
			'長度': length,
		}

		weight = material.material_density * .001 * (side_length_1 + side_length_2 - thickness) * thickness * length

	return render(request, 'measurer/result.html', {
		'shape': shape,
		'material': material,
		'weight_per_one_kg': weight,
		'weight_per_one_g': weight * 1000,
		'amount': amount,
		'total_weight_kg': weight * amount,
		'total_weight_g': weight * amount * 1000,
		'spec': spec
	})

def convert(unit, value):
	if unit == 'cm':
		return value
	else:
		return value*.1 if unit == 'mm' else value*100

def add_material(request):
	n = request.POST['new_name']
	d = float(request.POST['new_density'])

	m = Material(material_name=n, material_density=d
		)
	m.save()

	return HttpResponseRedirect(reverse('index'))

def display_material(request):
	materials = Material.objects.all()

	return render(request, 'measurer/list_material.html', {
		'materials': materials
	})