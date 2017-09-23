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
        lnum = request.POST["lote"]
        lote = Lote.objects.filter(pk=lnum)[0]
        years = []

        now = datetime.datetime.now()
        first_year = now.year + lote.edad

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
            loteMIE = rel[0].bp.MIE(lote.edad, 0, 0)
            data = {
                "ok": True,
                "riesgo":lote.riesgo.getValues(),
                "ingresos":[i * lote.area for i in loteMIE[1]],
                "egresos":[i * lote.area for i in loteMIE[2]],
                "margen":[i * lote.area for i in loteMIE[0]],
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
            return redirect('login')
        else:
            errors = form.errors
    template_name = 'register.html'
    context = {"form":form, "errors":errors, "mensage": mensaje}
    return render(request, template_name, context)

@login_required()
def updateProfile(request):
    print(request.POST)
    if request.method == "POST":
        form = EditUserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.gender = request.POST["gender"]
            user.save()
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
    context ={}

    fincas = request.user.finca_agricultor.all()
    if request.is_ajax():
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

                context = {"margen": margenTotal, "years":years}
                
            else:
                context = {"margen": [], "years":[]}
        else:
            context = {"margen": [], "years":[]}
        return HttpResponse(json.dumps(context), content_type="application/json")

    if fincas.__len__() == 0:
        context['warning'] = "No tienes ninguna finca, puedes crear una nueva haciendo click en 'CREAR FINCA'."

    context['fincas'] = fincas
    context['titulo'] = "Fincas"
    return render(request, "home_agricultor.html", context)

@login_required()
def home_admin(request):
    if request.user.role != 'A':
        return RedirectToHome(request.user)

    template_name = "home_admin.html"

    ctx = {"users":User.objects.filter(role="S")}

    return render(request, template_name, ctx )

class createFinca(CreateView):
    form_class = AddFincaForm
    template_name = "createFinca.html"

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.agricultor = self.request.user
        obj.save()
        return redirect('createLote')

    def get_context_data(self, **kwargs):
        ctx = super(createFinca, self).get_context_data(**kwargs)
        ctx['titulo'] = "Crear nueva finca"
        return ctx

@login_required()
def deleteFinca(request):
    data ={}
    if request.is_ajax():
        fnum = request.POST["finca"]
        finca = Finca.objects.get(pk=fnum)
        finca.delete()
        data['message'] = "La finca ha sido eliminada exitosamente"
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required()
def updateFinca(request, var):
    data ={}
    finca = Finca.objects.get(pk=var)
    if request.method == "POST":
        fincaform = AddFincaForm(request.POST or None, instance=finca)
        if fincaform.is_valid():
            fincaform.save()
        return redirect('home_agricultor')

    data['finca'] = AddFincaForm(instance = finca)
    data['titulo'] = "Modificar finca"
    return render(request, "updateFinca.html", data)

@login_required()
def updateLote(request, var):
    data ={}
    lote = Lote.objects.get(pk=var)
    riesgo = lote.riesgo
    if request.method == "POST":
        loteform = AddLoteForm(request.POST or None, instance=lote)
        riesgoform = AddRiesgoForm(request.POST or None, instance=riesgo)

        if loteform.is_valid() and riesgoform.is_valid():
            lote = loteform.save(commit=False)
            lote_has_bp.objects.filter(lote=lote).delete()
            qbp = Base_presupuestal.objects.filter(tipo=lote.tipo, cultivo=lote.cultivo, variedad=lote.variedad)
            if qbp.__len__() != 0:
                bp= qbp[0]
                lhbp = lote_has_bp(lote = lote,bp = bp)
                lhbp.save()
            loteform.save()
            riesgoform.save()

        return redirect('home_agricultor')

    data['lote'] = AddLoteForm(instance = lote)
    data['riesgo'] = AddRiesgoForm(instance = riesgo)
    data['titulo'] = "Modificar lote"
    return render(request, "updateLote.html", data)

@login_required()
def deleteUser(request):
    data ={}
    if request.is_ajax():
        unum = request.POST["user"]
        user = User.objects.get(pk=unum)
        user.delete()
        data['message'] = "El usuario ha sido eliminado exitosamente"
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required()
def deleteLote(request):
    data ={}
    if request.is_ajax():
        fnum = request.POST["lote"]
        lote = Lote.objects.get(pk=fnum)
        lote.delete()
        data['message'] = "El lote ha sido eliminado exitosamente"
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required()
def createLote(request):
    template_name = "createLote.html"
    ctx = {}
    if request.POST:
        loteform = AddLoteForm(request.POST or None)
        riesgoform = AddRiesgoForm(request.POST or None)

        if loteform.is_valid() and riesgoform.is_valid():
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
            else:
                ctx["messageWarning"] = "No se ha asignado ninguna base presupuestal a el lote "+request.POST["name"]

            ctx["messageSuccess"] = "El lote "+request.POST["name"]+" ha sido creado exitosamente."

            if 'exit' in request.POST:
                return redirect('home_agricultor')
            else:
                ctx['titulo'] = "Crear nuevo lote"
                ctx['loteform'] = AddLoteForm
                ctx['loteform'].declared_fields['finca'].queryset = Finca.objects.filter(agricultor=request.user)
                ctx['riesgoform'] = AddRiesgoForm

    else:
        ctx['titulo'] = "Crear nuevo lote"
        ctx['loteform'] = AddLoteForm
        qset = Finca.objects.filter(agricultor=request.user)
        ctx['loteform'].declared_fields['finca'].queryset = qset
        ctx['loteform'].declared_fields['finca'].initial = qset[0]
        ctx['riesgoform'] = AddRiesgoForm
    return render(request, template_name, ctx)

@login_required()
def createbp(request):
    template_name = "base_presupuestal.html"
    ctx = {}
    if request.is_ajax():
        step =  request.POST["step"]
        if step == "1":
            ctx['Insumos generales'] = AddInsumos_generalesForm(prefix="ig").as_table()
        elif step == "2":
            ctx['Establecimiento'] = AddEstablecimientoForm(prefix="establecimiento").as_table()
        elif step == "3":
            ctx['Preparación'] = AddPreparacion_costosForm(prefix="preparacion").as_table()
        elif step == "4":
            ctx['Datos generales'] = AddDatos_generalesForm(prefix="datos_g").as_table()
        elif step == "5":
            cipc =[]
            for x in range(1,16):
                cipc.append(AddcipcForm(prefix="cipc"+str(x)).as_table())
            ctx['Costos indirectos de producción y comercialización'] = cipc
        elif step == "6":
            ctx['Distribución de calidad1form'] = AddPorcentaje_precioForm(prefix="pp1").as_table()
            ctx['Distribución de calidad2form'] = AddPorcentaje_precioForm(prefix="pp2").as_table()
            ctx['Distribución de calidad3form'] = AddPorcentaje_precioForm(prefix="pp3").as_table()
        elif step == "7":
            ctx['Producción'] = AddProduccionForm(prefix="produccion").as_table()
        elif step == "8":
            data_mo_siembra =[]
            for x in range(1,16):
                data_mo_siembra.append(AddData_moForm(prefix="mosimebra"+str(x)).as_table())
            ctx['Siembra'] = data_mo_siembra
        elif step == "9":
            data_mo_resiembra =[]
            for x in range(1,16):
                data_mo_resiembra.append(AddData_moForm(prefix="moresiembra"+str(x)).as_table())
            ctx['Resiembra'] = data_mo_resiembra
        elif step == "10":
            data_mo_lgc =[]
            for x in range(1,16):
                data_mo_lgc.append(AddData_moForm(prefix="molgc"+str(x)).as_table())
            ctx['Limpia-guadaña-calles'] = data_mo_lgc
        elif step == "11":
            data_mo_ah =[]
            for x in range(1,16):
                data_mo_ah.append(AddData_moForm(prefix="moah"+str(x)).as_table())
            ctx['Aplicación de herbicida'] = data_mo_ah
        elif step == "12":
            data_mo_plateo =[]
            for x in range(1,16):
                data_mo_plateo.append(AddData_moForm(prefix="moplateo"+str(x)).as_table())
            ctx['Plateo'] = data_mo_plateo
        elif step == "13":
            data_mo_fertilizacion =[]
            for x in range(1,16):
                data_mo_fertilizacion.append(AddData_moForm(prefix="mofertilizacion"+str(x)).as_table())
            ctx['Fertilización'] = data_mo_fertilizacion
        elif step == "14":
            data_mo_amo =[]
            for x in range(1,16):
                data_mo_amo.append(AddData_moForm(prefix="moamo"+str(x)).as_table())
            ctx['Aplicación de materia orgánica'] = data_mo_amo
        elif step == "15":
            data_mo_fungicidas =[]
            for x in range(1,16):
                data_mo_fungicidas.append(AddData_moForm(prefix="mofungicidas"+str(x)).as_table())
            ctx['Fungicidas'] = data_mo_fungicidas
        elif step == "16":
            data_mo_biocontroladores =[]
            for x in range(1,16):
                data_mo_biocontroladores.append(AddData_moForm(prefix="mobiocontroladores"+str(x)).as_table())#
            ctx['Biocontroladores'] = data_mo_biocontroladores
        elif step == "17":
            data_mo_aspersiones =[]
            for x in range(1,16):
                data_mo_aspersiones.append(AddData_moForm(prefix="moaspersiones"+str(x)).as_table())
            ctx['Aspersiones'] = data_mo_aspersiones
        elif step == "18":
            data_mo_tutorado =[]
            for x in range(1,16):
                data_mo_tutorado.append(AddData_moForm(prefix="motutorado"+str(x)).as_table())
            ctx['Tutorado'] = data_mo_tutorado
        elif step == "19":
            data_mo_podas =[]
            for x in range(1,16):
                data_mo_podas.append(AddData_moForm(prefix="mopodas"+str(x)).as_table())
            ctx['Podas'] = data_mo_podas
        elif step == "20":
            data_mo_rc =[]
            for x in range(1,16):
                data_mo_rc.append(AddData_moForm(prefix="morc"+str(x)).as_table())
            ctx['Recolección contrato'] = data_mo_rc
        elif step == "21":
            data_mo_rd =[]
            for x in range(1,16):
                data_mo_rd.append(AddData_moForm(prefix="mord"+str(x)).as_table())
            ctx['Recolección por día'] = data_mo_rd
        elif step == "22":
            materiaOrganica =[]
            for x in range(1,16):
                materiaOrganica.append(AddCostosForm(prefix="costosmo"+str(x)).as_table())
            ctx['Materia organica'] = materiaOrganica
        elif step == "23":
            herbicidaCalles =[]
            for x in range(1,16):
                herbicidaCalles.append(AddCostosForm(prefix="costoshc"+str(x)).as_table())
            ctx['Herbicida calles'] = herbicidaCalles
        elif step == "24":
            herbicidaPlatos =[]
            for x in range(1,16):
                herbicidaPlatos.append(AddCostosForm(prefix="costoshp"+str(x)).as_table())
            ctx['Herbicida platos'] = herbicidaPlatos
        elif step == "25":
            insecticidas =[]
            for x in range(1,16):
                insecticidas.append(AddCostosForm(prefix="costosinsecticidas"+str(x)).as_table())
            ctx['Insecticidas'] = insecticidas
        elif step == "26":
            fungicidas =[]
            for x in range(1,16):
                fungicidas.append(AddCostosForm(prefix="costosinsecticidas"+str(x)).as_table())
            ctx['Fungicidas'] = fungicidas
        elif step == "27":
            fertilizante =[]
            for x in range(1,16):
                fertilizante.append(AddCostosForm(prefix="costosfertilizante"+str(x)).as_table())
            ctx['Fertilizante'] = fertilizante
        elif step == "28":
            ridomil =[]
            for x in range(1,16):
                ridomil.append(AddCostosForm(prefix="costosridomil"+str(x)).as_table())
            ctx['Ridomil'] = ridomil
        elif step == "29":
            fertilizanteFoliar =[]
            for x in range(1,16):
                fertilizanteFoliar.append(AddCostosForm(prefix="costosff"+str(x)).as_table())
            ctx['Fertilizante foliar'] = fertilizanteFoliar
        elif step == "30":
            biocontroladores =[]
            for x in range(1,16):
                biocontroladores.append(AddCostosForm(prefix="costosbiocontroladores"+str(x)).as_table())
            ctx['Biocontroladores'] = biocontroladores
        elif step == "31":
            guadana =[]
            for x in range(1,16):
                guadana.append(AddCostosForm(prefix="costosguadana"+str(x)).as_table())
            ctx['Guadaña'] = guadana
        elif step == "32":
            selectores =[]
            for x in range(1,16):
                selectores.append(AddCostosForm(prefix="costosselectores"+str(x)).as_table())
            ctx['Selectores'] = selectores
        elif step == "33":
            bombasEspalda =[]
            for x in range(1,16):
                bombasEspalda.append(AddCostosForm(prefix="costosbe"+str(x)).as_table())
            ctx['Bombas espalda'] = bombasEspalda
        elif step == "34":
            bombasEstacionarias =[]
            for x in range(1,16):
                bombasEstacionarias.append(AddCostosForm(prefix="costosbet"+str(x)).as_table())
            ctx['Bombas estacionarias'] = bombasEstacionarias
        elif step == "35":
            canastillas =[]
            for x in range(1,16):
                canastillas.append(AddCostosForm(prefix="costoscanatillas"+str(x)).as_table())
            ctx['Canastillas'] = canastillas
        elif step == "36":
            herramientas =[]
            for x in range(1,16):
                herramientas.append(AddCostosForm(prefix="costosh"+str(x)).as_table())
            ctx['Herramientas'] = herramientas
        elif step == "37":
            lycra =[]
            for x in range(1,16):
                lycra.append(AddCostosForm(prefix="costoslycra"+str(x)).as_table())
            ctx['Lycra'] = lycra

        return HttpResponse(json.dumps(ctx), content_type="application/json")
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
        ctx['titulo'] = "Crear nueva base presupuestal"
        ctx['base_presupuestal'] = AddBase_presupuestalForm(prefix="bp")

    return render(request, template_name, ctx)

@login_required()
def updatebp(request):
    template_name = "update_bp.html"
    ctx ={}
    ctx['bps'] = chooseBD()
    ctx['titulo'] = "Consultar base presupuestal"
    if request.method == "POST":
        bpform = chooseBD(request.POST)
        if bpform.is_valid():
            keybp = bpform.cleaned_data['bp']
            ctx['bpelegida'] = keybp.getValues()
            return render(request, template_name, ctx)
        else:
            ctx['message'] = "error"
            return render(request, template_name, ctx)

    return render(request, template_name, ctx)

@login_required()
def deletebp(request):
    template_name = "delete_bp.html"
    ctx ={}
    ctx['bps'] = chooseBD()
    ctx['titulo'] = "Eliminar base presupuestal"
    if request.method == "POST":
        bpform = chooseBD(request.POST)
        if bpform.is_valid():
            keybp = bpform.cleaned_data['bp']
            lote_has_bp.objects.filter(bp = keybp).delete()
            Base_presupuestal.objects.filter(pk = keybp.id).delete()
            ctx['messages'] = "La base presupuestal ha sido eliminada exitosamente."
            return render(request, template_name, ctx)
        else:
            ctx['messagew'] = "error"
            return render(request, template_name, ctx)
    return render(request, template_name, ctx)

def createUser(request):
    template_name = 'createUser.html'
    form = AddUserForm(request.POST or None)
    errors = None
    mensaje = None
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = True
            obj.role = 'S'
            obj.save()
            return redirect('login')
        else:
            errors = form.errors
    context = {"form":form, "errors":errors, "titulo": "Crear usuario"}
    return render(request, template_name, context)

def createAdmin(request):
    template_name = 'createAdmin.html'
    form = AddUserForm(request.POST or None)
    errors = None
    mensaje = None
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = True
            obj.role = 'A'
            obj.save()
            return redirect('login')
        else:
            errors = form.errors
    context = {"form":form, "errors":errors, "titulo": "Crear administrador"}
    return render(request, template_name, context)

@login_required()
def deleteAdmin(request):
    data ={}
    if request.is_ajax():
        unum = request.POST["user"]
        user = User.objects.get(pk=unum)
        user.delete()
        data['message'] = "El administrador ha sido eliminado exitosamente"
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required()
def home_root(request):
    if request.user.role != 'X':
        return RedirectToHome(request.user)

    template_name = "home_root.html"

    ctx = {"users":User.objects.filter(role='A')}

    return render(request, template_name, ctx )