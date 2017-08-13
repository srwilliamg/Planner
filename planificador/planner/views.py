# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from planner.util import *
from planner.forms import *
from planner.models import *
import datetime

def log_in(request):
    data = {}
    print(request.user)
    if request.user.is_authenticated():
        return RedirectToHome(request.user)

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

def loteChart(request):
    if request.is_ajax():
        #fnum = request.POST["finca"]
        lnum = request.POST["lote"]
        lote = Lote.objects.filter(pk=lnum)[0]
        #lotes = finca[0].lote_finca.all()
        years = []

        now = datetime.datetime.now()
        first_year = now.year - lote.edad

        for year in range(15):
            years.append(year+first_year)

        rel = lote.lotebp_lote.all()
        if rel.__len__() == 0:
            data = {
                "ok": False,
                "riesgo":lote.riesgo.getValues()
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            loteIE = rel[0].bp.IngresosEgresos()
            data = {
                "ok": True,
                "riesgo":lote.riesgo.getValues(),
                "ingresos":[i * lote.area for i in loteIE["ingresos"]],
                "egresos":[i * lote.area for i in loteIE["egresos"]],
                "years":years
            }
            
        return HttpResponse(json.dumps(data), content_type="application/json")

def register(request):
    form = AddUserForm(request.POST or None)
    errors = None
    mensaje = None
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = True
            obj.role = 'S'
            obj.save()
            mensaje = ("El usuario ha sido registrado exitosamente.")
            return redirect('login')
        else:
            errors = form.errors
    template_name = 'register.html'
    context = {"form":form, "errors":errors, "mensage": mensaje}
    return render(request, template_name, context)

@login_required()
def updateProfile(request):
    if request.method == "POST":
        form = EditUserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print form.errors
    return render(request,'profile.html')

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
        context['lotes'] = lotes
        context['margen'] = [1] #Puesto para solucionar conficto con chart de finca 
        context['years'] = [1] #Puesto para solucionar conficto con chart de finca 
        return context

@login_required()
def home_agricultor(request):
    if request.user.role != 'S':
        return RedirectToHome(request.user)

    margenes = []
    margenTotal = []
    years = []
    edades = []

    fincas = request.user.finca_agricultor.all()

    for f in fincas:
        lotes = f.lote_finca.all()
        for l in lotes:
            edades.append(l.edad)

    maximo = max(edades)
    minimo = min(edades)
    totalyears = int(abs(minimo) + abs(maximo) + 15)
    now = datetime.datetime.now()
    first_year = now.year - abs(minimo)

    for x in range(totalyears):
        margenTotal.append(0)
        years.append(x+first_year)

    for f in fincas:
        lotes = f.lote_finca.all()
        for l in lotes:
            qbp = l.lotebp_lote.all()
            if qbp.__len__() !=0:
                bp = l.lotebp_lote.all()[0].bp
                margenes.append(
                    [i * l.area for i in bp.margen(l.edad, minimo, maximo)]
                    )

    for x in margenes:
        for counter,y in enumerate(x):
            margenTotal[counter] += y

    context = {"fincas":fincas, "margen": margenTotal, "years":years ,"titulo": ("Fincas")}
    return render(request, "home_agricultor.html", context)

@login_required()
def home_admin(request):
    if request.user.role != 'A':
        return RedirectToHome(request.user)
    return render(request, "home_admin.html")

class createFinca(CreateView):
    form_class = AddFincaForm
    template_name = "createFinca.html"

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.agricultor = self.request.user
        obj.save()
        return redirect('home_agricultor')

    def get_context_data(self, **kwargs):
        ctx = super(createFinca, self).get_context_data(**kwargs)
        ctx['titulo'] = "Crear nueva finca"
        return ctx

def createLote(request):
    form_class = AddLoteForm
    template_name = "createLote.html"
    ctx = {}
    if request.POST:
        loteform = AddLoteForm(request.POST or None)
        riesgoform = AddRiesgoForm(request.POST or None)

        objlote = loteform.save(commit=False)
        objlote.agricultor = request.user
        objriesgo = riesgoform.save()
        objlote.riesgo = objriesgo
        objlote.save()

        qbp = Base_presupuestal.objects.filter(tipo=objlote.tipo, cultivo=objlote.cultivo, variedad=objlote.variedad)
        if qbp.__len__() != 0:
            bp= qbp[0]
            lhbp = lote_has_bp(lote = objlote,bp = bp)
            lhbp.save()
        return redirect('home_agricultor')
    else:
        ctx['titulo'] = "Crear nuevo lote"
        ctx['loteform'] = AddLoteForm
        ctx['riesgoform'] = AddRiesgoForm
    return render(request, template_name, ctx)

def createbp(request):
    template_name = "base_presupuestal.html"
    ctx = {}
    if request.POST:
        print(request.POST)
        #loteform = AddLoteForm(request.POST or None)
        #riesgoform = AddRiesgoForm(request.POST or None)

        #objlote = loteform.save(commit=False)
        #objlote.agricultor = request.user
        #objriesgo = riesgoform.save()
        #objlote.riesgo = objriesgo
        #objlote.save()

        #qbp = Base_presupuestal.objects.filter(tipo=objlote.tipo, cultivo=objlote.cultivo, variedad=objlote.variedad)
        #if qbp.__len__() != 0:
        #    bp= qbp[0]
        #    lhbp = lote_has_bp(lote = objlote,bp = bp)
        #    lhbp.save()
        return redirect('createbp')
    else:
        cipc =[
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm,
         AddcipcForm
        ]

        data_manoobra = {}
        data_mo_siembra =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Siembra'] = data_mo_siembra
        data_mo_resiembra =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Resiembra'] = data_mo_resiembra
        data_mo_lgc =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Limpia-guadaña-calles'] = data_mo_lgc
        data_mo_ah =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Aplicación de herbicida'] = data_mo_ah
        data_mo_plateo =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Plateo'] = data_mo_plateo
        data_mo_fertilizacion =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Fertilización'] = data_mo_fertilizacion
        data_mo_amo =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Aplicación de materia orgánica'] = data_mo_amo
        data_mo_fungicidas =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Fungicidas'] = data_mo_fungicidas
        data_mo_biocontroladores =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Biocontroladores'] = data_mo_biocontroladores
        data_mo_aspersiones =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Aspersiones'] = data_mo_aspersiones
        data_mo_tutorado =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Tutorado'] = data_mo_tutorado
        data_mo_podas =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Podas'] = data_mo_podas
        data_mo_rc =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Recolección contrato'] = data_mo_rc
        data_mo_rd =[
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm,
            AddData_moForm
        ]
        data_manoobra['Recolección por día'] = data_mo_rd

        data_costos = {}
        materiaOrganica =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['materia organica'] = materiaOrganica
        herbicidaCalles =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['herbicida calles'] = herbicidaCalles
        herbicidaPlatos =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['herbicida platos'] = herbicidaPlatos
        insecticidas =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['insecticidas'] = insecticidas
        fungicidas =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['fungicidas'] = fungicidas
        fertilizante =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['fertilizante'] = fertilizante
        ridomil =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['ridomil'] = ridomil
        fertilizanteFoliar =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['fertilizante foliar'] = fertilizanteFoliar
        biocontroladores =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['biocontroladores'] = biocontroladores
        guadana =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['guadaña'] = guadana
        selectores =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['selectores'] = selectores
        bombasEspalda =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['bombas espalda'] = bombasEspalda
        bombasEstacionarias =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['bombas estacionarias'] = bombasEstacionarias
        canastillas =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['canastillas'] = canastillas
        herramientas =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['herramientas'] = herramientas
        lycra =[
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm,
            AddCostosForm
            ]
        data_costos['lycra'] = lycra

        ctx['titulo'] = "Crear nueva base presupuestal"
        ctx['establecimientoform'] = AddEstablecimientoForm
        ctx['manoobra'] = data_manoobra
        ctx['preparacionform'] = AddPreparacion_costosForm
        ctx['data_costos'] = data_costos
        ctx['datos_generalesform'] = AddDatos_generalesForm
        ctx['produccionform'] = AddProduccionForm
        ctx['porcentaje_precio1form'] = AddPorcentaje_precioForm
        ctx['porcentaje_precio2form'] = AddPorcentaje_precioForm
        ctx['porcentaje_precio3form'] = AddPorcentaje_precioForm
        ctx['cipc'] = cipc
        ctx['Insumos_generalesform'] = AddInsumos_generalesForm
    return render(request, template_name, ctx)


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