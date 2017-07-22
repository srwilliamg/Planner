# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group as Django_Group
from .models import *
from planner.models import *

admin.site.unregister(Django_Group)

# Register your models here.

'''class ProfileUser(admin.ModelAdmin):
    list_display = ["id", "document_type", "document_number", "gender",
                    "first_name", "last_name", "birthdate", "address", "phone",
                    "email", "role", "is_active", "join_date", "last_login"]

    class Meta:
        model = User

class ProfileFinca(admin.ModelAdmin):
    list_display = ["id", "name", "area", "agricultor"]

    class Meta:
        model = Finca


class ProfileRiesgo(admin.ModelAdmin):
    list_display = ["id", "mercado", "fitosanitario", "fluctuacion_precio", "administracion", "tecnologia", "mano_de_obra",
                    "clima", "perecedero", "agremiacion", "inseguridad"]

    class Meta:
        model = Riesgo

class ProfileLote(admin.ModelAdmin):
    list_display = ["id", "tipo", "cultivo", "variedad", "edad", "area", "finca", "riesgo"]

    class Meta:
        model = Lote

admin.site.register(User, ProfileUser)
admin.site.register(Finca, ProfileFinca)
admin.site.register(Riesgo, ProfileRiesgo)
admin.site.register(Lote, ProfileLote)'''

from django.apps import apps

for model in apps.get_app_config('planner').models.values():
    admin.site.register(model)
