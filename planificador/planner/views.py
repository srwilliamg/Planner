# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from planner.util import *
from planner.forms import *
from planner.models import *

@login_required()
def home(request):
    data = request.POST.dict()
    data.update({"is_active": False})
    form = AddUserForm(request.POST)
    message_success = None
    message_error = None

    if request.method == "POST":
        if form.is_valid():
            usuario = form.save()
            form = AddUserForm(None)
            message_success = ("Registro exitoso. Por favor espere a que un "
                               "administrador active su cuenta")
        else:
            message_error = form.errors

    return render(request, "base_user.html", {
        "form": form,
        "message_success": message_success,
        "message_error": message_error
    })

def log_in(request):
    data = {}
    print(request.user)
    if request.user.is_authenticated():
        return RedirectToHome(request.user)
    #print(request.POST)

    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print(user)

        if user is None:
            data["error"] = "Nombre de usuario o contraseña incorrectos."
            return render(request, "login.html", data)

        if user.is_active:
            login(request, user)
            data["success"] = "Login correcto"
            return RedirectToHome(user)
        else:
            data["error"] = "El usuario no esta activo o fué eliminado."

    return render(request, "login.html", data)

@login_required()
def log_out(request):
    logout(request)
    return redirect("login")

def register(request):
    form = AddUserForm(request.POST or None)
    errors = None
    mensaje = None
    if request.method == "POST":
        if form.is_valid():
            form.save()
            mensaje = ("El usuario ha sido registrado exitosamente.")
            redirect('login')
        else:
            errors = form.errors
    template_name = 'register.html'
    context = {"form":form, "errors":errors, "mensage": mensaje}
    return render(request, template_name, context)

'''class createUser(CreateView):
    form_class = AddUserForm
    template_name = "register.html"
    success_url = "/home/user"'''

class LoteListView(ListView):
    template_name = 'home_agricultor.html'
    def get_queryset(self):
        number = self.kwargs.get("var")
        if number:
            finca = Finca.objects.filter(pk=number)
            queryset = finca[0].lote_finca.all()
            if queryset.__len__() == 0:
                queryset = ["No tiene ningún lote"]
        else:
            queryset = Finca.objects.none()
        return queryset

    def get_context_data(self, *args, **kwargs):
        number = self.kwargs.get("var")
        context = super(LoteListView, self).get_context_data(*args, **kwargs)
        finca = Finca.objects.filter(pk=number)
        lotes = finca[0].lote_finca.all()
        context['titulo'] = ("Lotes")
        data = {}

        if lotes.__len__() == 0:
            return context
        else:
            for x in lotes:
                rel = x.lotebp_lote.all()
                if rel.__len__() == 0:
                    return context
                else:
                    loteIE = rel[0].bp.IngresosEgresos()
                    data[x.id] = {"lote":x, "ingresos":loteIE["ingresos"], "egresos":loteIE["egresos"]}
        
        context['data_lotes'] = data
        return context

class RiesgoListView(ListView):
    template_name = 'home_agricultor.html'
    context_object_name = 'riesgo_list'
    def get_queryset(self):
        number = self.kwargs.get("var")
        if number:
            queryset = Lote.objects.filter(pk=number)[0].riesgo
        else:
            queryset = Lote.objects.none()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(RiesgoListView, self).get_context_data(*args, **kwargs)
        context['titulo'] = ("Riesgos")
        return context

@login_required()
def home_agricultor(request):
    fincas = request.user.finca_agricultor.all()
    context = {"fincas":fincas, "titulo": ("Fincas")}
    return render(request, "home_agricultor.html", context)

@login_required()
def home_admin(request):
    return render(request, "home_admin.html")

################################################3
class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args,**kwargs)
        return context

@login_required()
def listLotes(request):
    template_name = 'home.html'
    queryset = Lote.objects.all()
    context = {"Lotes" : queryset}
    return render(request, template_name, context)


class LotesListView(ListView):
    queryset = Lote.objects.all()
    template_name = 'home.html'


class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'home.html'

class FincasListView(ListView):
    template_name = 'home.html'
    def get_queryset(self):
        number = self.kwargs.get("var")
        if number:
            queryset = Finca.objects.filter(
                Q(agricultor__document_number__icontains=number) | Q(agricultor__document_number__iexact=number)
            )
            if queryset.__len__() == 0:
                queryset = ["No tienes ninguna finca"]
        else:
            queryset = Finca.objects.none()
        return queryset

class FincasDetailView(DetailView):
    template_name = 'home.html'
    queryset = Finca.objects.all()

    def get_context_data(self, *args, **kwargs): #this is using pk like var in URL
        context = super(FincasDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs): #this is using 'key' like var in URL
        key = self.kwargs.get('key')
        obj = get_object_or_404(Finca, id=key)
        return obj
#############################################################3