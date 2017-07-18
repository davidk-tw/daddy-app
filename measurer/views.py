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
			'realname': '直徑',
			'list': ['tube']
		},
		'thickness': {
			'realname': '厚度',
			'list': ['tube', 'rectangular_tube', 'plate', 'angle', 'storage_tank_square', 'storage_tank_one', 'storage_tank_both']
		},
		'width': {
			'realname': '寬度',
			'list': ['plate', 'rectangular_tube', 'cuboid', 'storage_tank_square']
		},
		'length': {
			'realname': '長度',
			'list': ['tube', 'round_bar', 'plate', 'rectangular_tube', 'cuboid', 'hexagonal', 'octagonal', 'angle', 'channel', 'beam', 'storage_tank_square']
		},
		'height': {
			'realname': '高度',
			'list': ['rectangular_tube', 'cuboid', 'storage_tank_square', 'channel', 'beam', 'storage_tank_one', 'storage_tank_both']
		},
		'radius': {
			'realname': '半徑',
			'list': ['round_bar', ]
		},
		'diameter': {
			'realname': '直徑',
			'list': ['storage_tank_one', 'storage_tank_both']
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
		'bone_width': {
			'realname': '腰厚',
			'list': ['channel', 'beam']
		},
		'branch_length': {
			'realname': '腿長',
			'list': ['channel', 'beam']
		},
		'branch_width': {
			'realname': '平均腿厚',
			'list': ['channel', 'beam']
		},
		'innerarc_radius': {
			'realname': '內弧半徑',
			'list': ['channel', 'beam']
		},
		'edgearc_radius': {
			'realname': '端弧半徑',
			'list': ['channel', 'beam']
		}
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
		outer_radius = unitconv(request.POST['outer_radius-unit'], float(request.POST['outer_radius']))
		thickness = unitconv(request.POST['thickness-unit'], float(request.POST['thickness']))
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))

		spec = {
			'直徑': outer_radius,
			'厚度': thickness,
			'長度': length
		}

		weight = material.material_density * .001 * (outer_radius - thickness) * thickness * math.pi * length

	elif shape.shape_name == 'round_bar':
		radius = unitconv(request.POST['radius-unit'], float(request.POST['radius']))
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))

		spec = {
			'半徑': radius,
			'長度': length
		}

		weight = material.material_density * .001 * pow(radius, 2) * length * math.pi

	elif shape.shape_name == 'plate':
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		thickness = unitconv(request.POST['thickness-unit'], float(request.POST['thickness']))
		width = unitconv(request.POST['width-unit'], float(request.POST['width']))

		spec = {
			'長度': length,
			'厚度': thickness,
			'寬度': width
		}

		weight = material.material_density * .001 * length * width * thickness

	elif shape.shape_name == 'rectangular_tube':
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		width = unitconv(request.POST['width-unit'], float(request.POST['width']))
		thickness = unitconv(request.POST['thickness-unit'], float(request.POST['thickness']))
		height = unitconv(request.POST['height-unit'], float(request.POST['height']))
		
		spec = {
			'長度': length,
			'寬度': width,
			'高度': height,
			'厚度': thickness,
		}

		weight = material.material_density * .001 * (length + width) * 2 * height

	elif shape.shape_name == 'cuboid':
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		width = unitconv(request.POST['width-unit'], float(request.POST['width']))
		height = unitconv(request.POST['height-unit'], float(request.POST['height']))
		
		spec = {
			'長度': length,
			'寬度': width,
			'高度': height,
		}

		weight = material.material_density * .001 * length * width * height

	elif shape.shape_name == 'hexagonal' or shape.shape_name == 'octagonal':
		const = .866 if shape.shape_name == 'hexagonal' else .828
		diagonal = unitconv(request.POST['diagonal-unit'], float(request.POST['diagonal']))
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		
		spec = {
			'長度': length,
			'對角線長度': diagonal
		}

		weight = material.material_density * .001 * pow(diagonal, 2) * length * const

	elif shape.shape_name == 'angle':
		side_length_1 = unitconv(request.POST['side_length_1-unit'], float(request.POST['side_length_1']))
		side_length_2 = unitconv(request.POST['side_length_2-unit'], float(request.POST['side_length_2']))
		thickness = unitconv(request.POST['thickness-unit'], float(request.POST['thickness']))
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		
		spec = {
			'邊長-1': side_length_1,
			'邊長-2': side_length_2,
			'厚度': thickness,
			'長度': length,
		}

		weight = material.material_density * .001 * (side_length_1 + side_length_2 - thickness) * thickness * length

	elif shape.shape_name == 'channel' or shape.shape_name == 'beam':
		const = .349 if shape.shape_name == 'channel' else .615
		height = unitconv(request.POST['height-unit'], float(request.POST['height']))
		bone_width = unitconv(request.POST['bone_width-unit'], float(request.POST['bone_width']))
		branch_width = unitconv(request.POST['branch_width-unit'], float(request.POST['branch_width']))
		branch_length = unitconv(request.POST['branch_length-unit'], float(request.POST['branch_length']))
		innerarc_radius = unitconv(request.POST['innerarc_radius-unit'], float(request.POST['innerarc_radius']))
		edgearc_radius = unitconv(request.POST['edgearc_radius-unit'], float(request.POST['edgearc_radius']))
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		
		spec = {
			'高度': height,
			'腰厚': bone_width,
			'平均腿厚': branch_width,
			'腿長': branch_length,
			'內弧半徑': innerarc_radius,
			'端弧半徑': edgearc_radius,
			'長度': length,
		}

		weight = material.material_density * .001 * (height*bone_width + 2*branch_width*(branch_length-bone_width) + const*(pow(innerarc_radius, 2)-pow(edgearc_radius, 2))) * length

	elif shape.shape_name == 'storage_tank_square':
		thickness = unitconv(request.POST['thickness-unit'], float(request.POST['thickness']))
		length = unitconv(request.POST['length-unit'], float(request.POST['length']))
		height = unitconv(request.POST['height-unit'], float(request.POST['height']))
		width = unitconv(request.POST['width-unit'], float(request.POST['width']))
		
		spec = {
			'長度': length,
			'寬度': width,
			'高度': height,
			'厚度': thickness
		}

		weight = (length * width * height - ((length - thickness*2) * (width - thickness*2)*(height-thickness)) * material.material_density) * .001

	elif shape.shape_name == 'storage_tank_one' or shape.shape_name == 'storage_tank_both':
		thickness = unitconv(request.POST['thickness-unit'], float(request.POST['thickness']))
		height = unitconv(request.POST['height-unit'], float(request.POST['height']))
		diameter = unitconv(request.POST['diameter-unit'], float(request.POST['diameter']))
		radius = diameter / 2.0

		spec = {
			'高度': height,
			'厚度': thickness,
			'直徑': diameter
		}
		bottom = 1 if shape.shape_name == 'storage_tank_one' else 2
		weight = ((diameter - thickness)*thickness*height*math.pi + math.pi*pow(radius, 2)*thickness*2) * .001 * material.material_density

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


def unitconv(unit, value):
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