  # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from views import *

urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^home/$', LotesListView.as_view()),
    #url(r'^home/user/$', UserListView.as_view()),
    #rl(r'^home/finca/ver/(?P<key>\w+)/$', FincasDeta#ilView.as_view()),
    url(r'^$', views.log_in, name='index'),
    url(r'^index/$', TemplateView.as_view(template_name = 'index.html'), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name="logout"),
    url(r'^profile/$', views.updateProfile, name="profile"),
    url(r'^home_agricultor/$', views.home_agricultor, name='home_agricultor'),
    url(r'^home_agricultor/finca/chart/$', views.fincaChart, name='fincaChart'),
    url(r'^home_agricultor/lotes/(?P<var>\w+)/$', LoteListView.as_view(), name='lotes'),
    url(r'^home_agricultor/lotes/\d+/loteChart/$', views.loteChart, name='loteChart'),
    url(r'^home_admin/$', views.home_admin, name='home_admin'),
    url(r'^home_admin/deleteuser/$', views.deleteUser, name='deleteUser'),
    url(r'^home_agricultor/crearf/$', createFinca.as_view(), name = "createFinca"),
    url(r'^home_agricultor/deletef/$', views.deleteFinca, name = "deleteFinca"),
    url(r'^home_agricultor/updatef/(?P<var>\d+)/$', views.updateFinca, name='updateFinca'),
    url(r'^home_agricultor/crearl/$', views.createLote, name = "createLote"),
    url(r'^home_agricultor/deletel/$', views.deleteLote, name = "deleteLote"),
    url(r'^home_agricultor/updatel/(?P<var>\d+)/$', views.updateLote, name='updateLote'),
    url(r'^home_agricultor/crearbp/$', views.createbp, name = "createbp"),
    url(r'^home_agricultor/updatebp/$', views.updatebp, name = "updatebp"),
    url(r'^home_agricultor/deletebp/$', views.deletebp, name = "deletebp"),
]
