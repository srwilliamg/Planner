from django import template
import datetime

register = template.Library()

@register.filter
def anioSiembra(value):
	now = datetime.datetime.now()
	year = now.year
	return int(year + value)

@register.filter
def completeRol(value):
	if "R" == value:
		return "RealRoot"
	elif "A" == value:
		return "Administrador"
	elif "S" == value:
		return "Agricultor"
	elif "X" == value:
		return "Root"
	else:
		return "Indefinido"

@register.filter
def completeGender(value):
	if "M" == value:
		return "Masculino"
	elif "F" == value:
		return "Femenino"
	elif "O" == value:
		return "Otro"
	else:
		return "Indefinido"