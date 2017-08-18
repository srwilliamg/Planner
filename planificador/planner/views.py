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
        #print(user)

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

@login_required()
def fincaChart(request):
    data = {}
    margenes = []
    ingresos = []
    egresos = []
    margenTotal = []
    ingresosTotal = []
    egresosTotal = []
    years = []
    edades = []

    if request.is_ajax():
        lnum = request.POST["finca"]
        finca = Finca.objects.filter(pk=lnum)[0]
        print(finca)

        lotes = finca.lote_finca.all()
        for l in lotes:
            edades.append(l.edad)

        if len(edades)!= 0:
            maximo = max(edades)
            minimo = min(edades)
            totalyears = int(abs(minimo) + abs(maximo) + 15)
            now = datetime.datetime.now()
            first_year = now.year - abs(minimo)

            for x in range(totalyears):
                margenTotal.append(0)
                ingresosTotal.append(0)
                egresosTotal.append(0)
                years.append(x+first_year)

            lotes = finca.lote_finca.all()
            for l in lotes:
                qbp = l.lotebp_lote.all()
                if qbp.__len__() !=0:
                    bp = l.lotebp_lote.all()[0].bp
                    MIE = bp.MIE(l.edad, minimo, maximo)
                    margenes.append(
                        [i * l.area for i in MIE[0]]
                    )
                    ingresos.append(
                        [i * l.area for i in MIE[1]]
                    )
                    egresos.append(
                        [i * l.area for i in MIE[2]]
                    )

            for x in margenes:
                for counter,y in enumerate(x):
                    margenTotal[counter] += y

            for i in ingresos:
                for c,i in enumerate(i):
                    ingresosTotal[c] += i

            for e in egresos:
                for cont,w in enumerate(e):
                    egresosTotal[cont] += w

            if len(margenTotal) == 0:
                print("Was false")
                data = {
                    "ok": False,
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                print("was true")
                data = {
                    "ok": True,
                    "ingresos":ingresosTotal,
                    "egresos":egresosTotal,
                    "margen": margenTotal,
                    "years":years
                }

        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required()
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
    if fincas.__len__() != 0:
        for f in fincas:
            lotes = f.lote_finca.all()
            for l in lotes:
                edades.append(l.edad)
        if len(edades)!= 0:
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
        else:
            context = {"fincas":fincas, "margen": [], "years":[] ,"titulo": ("Fincas")}
    else:
        context = {"fincas":[], "margen": [], "years":[],"titulo": ("Fincas")}
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

@login_required()
def createLote(request):
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
        ctx['loteform'].declared_fields['finca'].queryset = Finca.objects.filter(agricultor=request.user)
        ctx['riesgoform'] = AddRiesgoForm
    return render(request, template_name, ctx)

@login_required()
def createbp(request):
    template_name = "base_presupuestal.html"
    ctx = {}
    if request.POST:
        #print(request.POST)
        cipc =[]
        data_mo_siembra =[]
        data_mo_resiembra =[]
        data_mo_lgc =[]
        data_mo_ah =[]
        data_mo_plateo =[]
        data_mo_fertilizacion =[]
        data_mo_amo =[]
        data_mo_fungicidas =[]
        data_mo_biocontroladores =[]
        data_mo_aspersiones =[]
        data_mo_tutorado =[]
        data_mo_podas =[]
        data_mo_rc =[]
        data_mo_rd =[]
        materiaOrganica =[]
        herbicidaCalles =[]
        herbicidaPlatos =[]
        insecticidas =[]
        fungicidas =[]
        fertilizante =[]
        ridomil =[]
        fertilizanteFoliar =[]
        biocontroladores =[]
        guadana =[]
        selectores =[]
        bombasEspalda =[]
        bombasEstacionarias =[]
        canastillas =[]
        herramientas =[]
        lycra =[]

        bp = AddBase_presupuestalForm(request.POST, prefix="bp").save(commit=False)

        for x in range(1,16):
            cipc.append(AddcipcForm(request.POST, prefix="cipc"+str(x)).save())

            data_mo_siembra.append(AddData_moForm(request.POST, prefix="mosimebra"+str(x)).save())
            data_mo_resiembra.append(AddData_moForm(request.POST, prefix="moresiembra"+str(x)).save())
            data_mo_lgc.append(AddData_moForm(request.POST, prefix="molgc"+str(x)).save())
            data_mo_ah.append(AddData_moForm(request.POST, prefix="moah"+str(x)).save())
            data_mo_plateo.append(AddData_moForm(request.POST, prefix="moplateo"+str(x)).save())
            data_mo_fertilizacion.append(AddData_moForm(request.POST, prefix="mofertilizacion"+str(x)).save())
            data_mo_amo.append(AddData_moForm(request.POST, prefix="moamo"+str(x)).save())
            data_mo_fungicidas.append(AddData_moForm(request.POST, prefix="mofungicidas"+str(x)).save())
            data_mo_biocontroladores.append(AddData_moForm(request.POST, prefix="mobiocontroladores"+str(x)).save())
            data_mo_aspersiones.append(AddData_moForm(request.POST, prefix="moaspersiones"+str(x)).save())
            data_mo_tutorado.append(AddData_moForm(request.POST, prefix="motutorado"+str(x)).save())
            data_mo_podas.append(AddData_moForm(request.POST, prefix="mopodas"+str(x)).save())
            data_mo_rc.append(AddData_moForm(request.POST, prefix="morc"+str(x)).save())
            data_mo_rd.append(AddData_moForm(request.POST, prefix="mord"+str(x)).save())

            materiaOrganica.append(AddCostosForm(request.POST, prefix="costosmo"+str(x)).save())
            herbicidaCalles.append(AddCostosForm(request.POST, prefix="costoshc"+str(x)).save())
            herbicidaPlatos.append(AddCostosForm(request.POST, prefix="costoshp"+str(x)).save())
            insecticidas.append(AddCostosForm(request.POST, prefix="costosinsecticidas"+str(x)).save())
            fungicidas.append(AddCostosForm(request.POST, prefix="costosinsecticidas"+str(x)).save())
            fertilizante.append(AddCostosForm(request.POST, prefix="costosfertilizante"+str(x)).save())
            ridomil.append(AddCostosForm(request.POST, prefix="costosridomil"+str(x)).save())
            fertilizanteFoliar.append(AddCostosForm(request.POST, prefix="costosff"+str(x)).save())
            biocontroladores.append(AddCostosForm(request.POST, prefix="costosbiocontroladores"+str(x)).save())
            guadana.append(AddCostosForm(request.POST, prefix="costosguadana"+str(x)).save())
            selectores.append(AddCostosForm(request.POST, prefix="costosselectores"+str(x)).save())
            bombasEspalda.append(AddCostosForm(request.POST, prefix="costosbe"+str(x)).save())
            bombasEstacionarias.append(AddCostosForm(request.POST, prefix="costosbet"+str(x)).save())
            canastillas.append(AddCostosForm(request.POST, prefix="costoscanatillas"+str(x)).save())
            herramientas.append(AddCostosForm(request.POST, prefix="costosh"+str(x)).save())
            lycra.append(AddCostosForm(request.POST, prefix="costoslycra"+str(x)).save())


        #Guardando datos de costo de insumos
        ci = [materiaOrganica, herbicidaCalles, herbicidaPlatos, insecticidas, fungicidas, fertilizante, ridomil, 
                fertilizanteFoliar, biocontroladores, guadana, selectores, bombasEspalda, bombasEstacionarias, 
                canastillas, herramientas, lycra]

        ci_ano =[]
        for obj in ci:
            ano = Ano_costo()
            ano.ano1 = obj[0]
            ano.ano2 = obj[1]
            ano.ano3 = obj[2]
            ano.ano4 = obj[3]
            ano.ano5 = obj[4]
            ano.ano6 = obj[5]
            ano.ano7 = obj[6]
            ano.ano8 = obj[7]
            ano.ano9 = obj[8]
            ano.ano10 = obj[9]
            ano.ano11 = obj[10]
            ano.ano12 = obj[11]
            ano.ano13 = obj[12]
            ano.ano14 = obj[13]
            ano.ano15 = obj[14]
            ano.save()
            ci_ano.append(ano)

        cCI = Costos_insumos(
            materiaOrganica = ci_ano[0],
            herbicidaCalles = ci_ano[1],
            herbicidaPlatos = ci_ano[2],
            insecticidas = ci_ano[3],
            fungicidas = ci_ano[4],
            fertilizante = ci_ano[5],
            ridomil = ci_ano[6],
            fertilizanteFoliar = ci_ano[7],
            biocontroladores = ci_ano[8],
            guadana = ci_ano[9],
            selectores = ci_ano[10],
            bombasEspalda = ci_ano[11],
            bombasEstacionarias = ci_ano[12],
            canastillas = ci_ano[13],
            herramientas = ci_ano[14],
            lycra = ci_ano[15]
            )
        cCI.save()

        #Guardando datos de Insumos de mano de obra

        i_mo = [
            data_mo_siembra,
            data_mo_resiembra,
            data_mo_lgc,
            data_mo_ah,
            data_mo_plateo,
            data_mo_fertilizacion,
            data_mo_amo,
            data_mo_fungicidas,
            data_mo_biocontroladores,
            data_mo_aspersiones,
            data_mo_tutorado,
            data_mo_podas,
            data_mo_rc,
            data_mo_rd
        ]

        imo_ano =[]
        for data in i_mo:
            anomo = Anos_mo()
            anomo.ano1 = data[0]
            anomo.ano2 = data[1]
            anomo.ano3 = data[2]
            anomo.ano4 = data[3]
            anomo.ano5 = data[4]
            anomo.ano6 = data[5]
            anomo.ano7 = data[6]
            anomo.ano8 = data[7]
            anomo.ano9 = data[8]
            anomo.ano10 = data[9]
            anomo.ano11 = data[10]
            anomo.ano12 = data[11]
            anomo.ano13 = data[12]
            anomo.ano14 = data[13]
            anomo.ano15 = data[14]
            anomo.save()
            imo_ano.append(anomo)

        c_IMO = Insumos_mo(
            siembra = imo_ano[0],
            resiembra = imo_ano[1],
            limpiaGuadanaCalles = imo_ano[2],
            aplicacionHerbicida = imo_ano[3],
            plateo = imo_ano[4],
            fertilizacion = imo_ano[5],
            aplicacionMateriaOrganica = imo_ano[6],
            fungicidas = imo_ano[7],
            biocontroladores = imo_ano[8],
            aspersiones = imo_ano[9],
            tutorado = imo_ano[10],
            podas = imo_ano[11],
            recoleccionContrato = imo_ano[12],
            recoleccionDia = imo_ano[13]
            )

        c_IMO.save()

        #Guardando datos de CIPC
        cCIPC = Ano_cipc(ano1 = cipc[0], ano2 = cipc[1], ano3 = cipc[2], ano4 = cipc[3], ano5 = cipc[4], 
                ano6 = cipc[5], ano7 = cipc[6], ano8 = cipc[7], ano9 = cipc[8], ano10 = cipc[9], 
                ano11 = cipc[10], ano12 = cipc[11], ano13 = cipc[12], ano14 = cipc[13], 
                ano15 = cipc[14])
        cCIPC.save()

        cestablecimiento = AddEstablecimientoForm(request.POST, prefix="establecimiento").save()#

        cpreparacion = AddPreparacion_costosForm(request.POST, prefix="preparacion").save()#

        cdatos_generales = AddDatos_generalesForm(request.POST, prefix="datos_g").save()#

        produccion = AddProduccionForm(request.POST, prefix="produccion").save()#
        porcentaje_precio1 = AddPorcentaje_precioForm(request.POST, prefix="pp1").save()#
        porcentaje_precio2 = AddPorcentaje_precioForm(request.POST, prefix="pp2").save()#
        porcentaje_precio3 = AddPorcentaje_precioForm(request.POST, prefix="pp3").save()#
        cDC = Distribucion_calidad(
            primera = porcentaje_precio1,
            segunda = porcentaje_precio2,
            tercera = porcentaje_precio3,
            produccion = produccion
        )#
        cDC.save()

        cInsumos_generales = AddInsumos_generalesForm(request.POST, prefix="ig").save() #

        bp.datos_g = cdatos_generales
        bp.insumos_g = cInsumos_generales
        bp.preparacion = cpreparacion
        bp.costos_insumos = cCI
        bp.insumos_mo = c_IMO
        bp.distribucion_calidad = cDC 
        bp.establecimiento_r = cestablecimiento
        bp.cipc = cCIPC

        bp.save()

        return redirect('home_agricultor')
    else:
        cipc =[]
        data_mo_siembra =[]
        data_mo_resiembra =[]
        data_mo_lgc =[]
        data_mo_ah =[]
        data_mo_plateo =[]
        data_mo_fertilizacion =[]
        data_mo_amo =[]
        data_mo_fungicidas =[]
        data_mo_biocontroladores =[]
        data_mo_aspersiones =[]
        data_mo_tutorado =[]
        data_mo_podas =[]
        data_mo_rc =[]
        data_mo_rd =[]
        materiaOrganica =[]
        herbicidaCalles =[]
        herbicidaPlatos =[]
        insecticidas =[]
        fungicidas =[]
        fertilizante =[]
        ridomil =[]
        fertilizanteFoliar =[]
        biocontroladores =[]
        guadana =[]
        selectores =[]
        bombasEspalda =[]
        bombasEstacionarias =[]
        canastillas =[]
        herramientas =[]
        lycra =[]

        for x in range(1,16):
            cipc.append(AddcipcForm(prefix="cipc"+str(x)))
            data_mo_siembra.append(AddData_moForm(prefix="mosimebra"+str(x)))
            data_mo_resiembra.append(AddData_moForm(prefix="moresiembra"+str(x)))
            data_mo_lgc.append(AddData_moForm(prefix="molgc"+str(x)))
            data_mo_ah.append(AddData_moForm(prefix="moah"+str(x)))
            data_mo_plateo.append(AddData_moForm(prefix="moplateo"+str(x)))
            data_mo_fertilizacion.append(AddData_moForm(prefix="mofertilizacion"+str(x)))
            data_mo_amo.append(AddData_moForm(prefix="moamo"+str(x)))
            data_mo_fungicidas.append(AddData_moForm(prefix="mofungicidas"+str(x)))
            data_mo_biocontroladores.append(AddData_moForm(prefix="mobiocontroladores"+str(x)))
            data_mo_aspersiones.append(AddData_moForm(prefix="moaspersiones"+str(x)))
            data_mo_tutorado.append(AddData_moForm(prefix="motutorado"+str(x)))
            data_mo_podas.append(AddData_moForm(prefix="mopodas"+str(x)))
            data_mo_rc.append(AddData_moForm(prefix="morc"+str(x)))
            data_mo_rd.append(AddData_moForm(prefix="mord"+str(x)))
            materiaOrganica.append(AddCostosForm(prefix="costosmo"+str(x)))
            herbicidaCalles.append(AddCostosForm(prefix="costoshc"+str(x)))
            herbicidaPlatos.append(AddCostosForm(prefix="costoshp"+str(x)))
            insecticidas.append(AddCostosForm(prefix="costosinsecticidas"+str(x)))
            fungicidas.append(AddCostosForm(prefix="costosinsecticidas"+str(x)))
            fertilizante.append(AddCostosForm(prefix="costosfertilizante"+str(x)))
            ridomil.append(AddCostosForm(prefix="costosridomil"+str(x)))
            fertilizanteFoliar.append(AddCostosForm(prefix="costosff"+str(x)))
            biocontroladores.append(AddCostosForm(prefix="costosbiocontroladores"+str(x)))
            guadana.append(AddCostosForm(prefix="costosguadana"+str(x)))
            selectores.append(AddCostosForm(prefix="costosselectores"+str(x)))
            bombasEspalda.append(AddCostosForm(prefix="costosbe"+str(x)))
            bombasEstacionarias.append(AddCostosForm(prefix="costosbet"+str(x)))
            canastillas.append(AddCostosForm(prefix="costoscanatillas"+str(x)))
            herramientas.append(AddCostosForm(prefix="costosh"+str(x)))
            lycra.append(AddCostosForm(prefix="costoslycra"+str(x)))


        data_manoobra = {}
        
        data_manoobra['Siembra'] = data_mo_siembra
        data_manoobra['Resiembra'] = data_mo_resiembra
        data_manoobra['Limpia-guadaña-calles'] = data_mo_lgc
        data_manoobra['Aplicación de herbicida'] = data_mo_ah
        data_manoobra['Plateo'] = data_mo_plateo
        data_manoobra['Fertilización'] = data_mo_fertilizacion
        data_manoobra['Aplicación de materia orgánica'] = data_mo_amo
        data_manoobra['Fungicidas'] = data_mo_fungicidas
        data_manoobra['Biocontroladores'] = data_mo_biocontroladores
        data_manoobra['Aspersiones'] = data_mo_aspersiones
        data_manoobra['Tutorado'] = data_mo_tutorado
        data_manoobra['Podas'] = data_mo_podas
        data_manoobra['Recolección contrato'] = data_mo_rc
        data_manoobra['Recolección por día'] = data_mo_rd

        data_costos = {}
        
        data_costos['materia organica'] = materiaOrganica
        data_costos['herbicida calles'] = herbicidaCalles
        data_costos['herbicida platos'] = herbicidaPlatos
        data_costos['insecticidas'] = insecticidas
        data_costos['fungicidas'] = fungicidas
        data_costos['fertilizante'] = fertilizante
        data_costos['ridomil'] = ridomil
        data_costos['fertilizante foliar'] = fertilizanteFoliar
        data_costos['biocontroladores'] = biocontroladores
        data_costos['guadaña'] = guadana
        data_costos['selectores'] = selectores
        data_costos['bombas espalda'] = bombasEspalda
        data_costos['bombas estacionarias'] = bombasEstacionarias
        data_costos['canastillas'] = canastillas
        data_costos['herramientas'] = herramientas
        data_costos['lycra'] = lycra

        ctx['titulo'] = "Crear nueva base presupuestal"
        ctx['establecimientoform'] = AddEstablecimientoForm(prefix="establecimiento")
        ctx['manoobra'] = data_manoobra
        ctx['preparacionform'] = AddPreparacion_costosForm(prefix="preparacion")
        ctx['data_costos'] = data_costos
        ctx['datos_generalesform'] = AddDatos_generalesForm(prefix="datos_g")
        ctx['produccionform'] = AddProduccionForm(prefix="produccion")
        ctx['porcentaje_precio1form'] = AddPorcentaje_precioForm(prefix="pp1")
        ctx['porcentaje_precio2form'] = AddPorcentaje_precioForm(prefix="pp2")
        ctx['porcentaje_precio3form'] = AddPorcentaje_precioForm(prefix="pp3")
        ctx['cipc'] = cipc
        ctx['Insumos_generalesform'] = AddInsumos_generalesForm(prefix="ig")
        ctx['base_presupuestal'] = AddBase_presupuestalForm(prefix="bp")

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
        #print(context)
        return context

    def get_object(self, *args, **kwargs): #this is using 'key' like var in URL
        key = self.kwargs.get('key')
        obj = get_object_or_404(Finca, id=key)
        return obj
#############################################################3