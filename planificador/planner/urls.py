from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from views import *

urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^home/$', LotesListView.as_view()),
    #url(r'^home/user/$', UserListView.as_view()),
    #url(r'^home/finca/(?P<var>\w+)/$', FincasListView.as_view()),
    #rl(r'^home/finca/ver/(?P<key>\w+)/$', FincasDeta#ilView.as_view()),
    url(r'^$', views.log_in, name='index'),
    url(r'^index/$', TemplateView.as_view(template_name = 'index.html'), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name="logout"),
    url(r'^profile/$', views.updateProfile, name="profile"),
    url(r'^home_agricultor/$', views.home_agricultor, name='home_agricultor'),
    url(r'^home_agricultor/lotes/(?P<var>\w+)/$', LoteListView.as_view(), name='lotes'),
    url(r'^home_agricultor/riesgo/(?P<var>\w+)/$', RiesgoListView.as_view(), name='riesgo'),
    url(r'^home_admin/$', views.home_admin, name='home_admin'),
]
