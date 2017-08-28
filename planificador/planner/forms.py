# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import *


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "document_number",
            "document_type",
            "email",
            "password",
            "first_name",
            "last_name",
            "birthdate",
            "gender",
            "address",
            "phone"
            #"role",
            #"is_active"
        ]

    document_number = forms.CharField(
        required=True, label="Número de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Número de documento", "class": "form-control"}))

    document_type = forms.ChoiceField(
        required=True, label= "Tipo de documento", widget=forms.RadioSelect(attrs={"title": "Tipo de documento","class": "radio-inline"}), choices=DOCUMENT_OPTIONS)

    gender = forms.ChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), choices=GENDER_OPTIONS)

    first_name = forms.CharField(
        required=True, widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre", "class": "form-control"}),
        label="Primer Nombre"
    )

    last_name = forms.CharField(
        required=True, label="Apellido",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Apellido", "class": "form-control"}))

    birthdate = forms.DateField(
        required=True, label="Fecha de nacimiento",
        input_formats=["%Y-%m-%d",
                       "%d/%m/%Y",
                       "%d/%m/%y"], widget=forms.TextInput(attrs={"placeholder": "Día/Mes/Año","class": "form-control"})
    )

    address = forms.CharField(
        required=True, label="Dirección de Residencia",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Dirección de Residencia", "class": "form-control"}
        ))
    phone = forms.CharField(
        required=True, label="Número de teléfono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de teléfono", "class": "form-control"}
        ))

    email = forms.EmailField(
        required=True, label="Email", widget=forms.TextInput(attrs={"placeholder": "example@example.co","class": "form-control"}))
    password = forms.CharField(
        required=True, label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    #role = forms.ChoiceField(
    #    required=True, label="Rol", widget=forms.Select(attrs={"class": "form-control"}), choices=ROLE_OPTIONS)

    #is_active = forms.BooleanField(required=True, label="Es usuario activo")

class AddAgricultorForm(AddUserForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        initial.update({"role": "S"})
        super(AddAgricultorForm, self).__init__(args, kwargs)

class AddAdministratorForm(AddUserForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        initial.update({"role": "A"})
        super(AddAdministratorForm, self).__init__(args, kwargs)

class AddFincaForm(forms.ModelForm):
    class Meta:
        model = Finca
        fields = ['name', 'area']

    name = forms.CharField(
        required=True, label="Nombre",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control", "placeholder":"Nombre de la finca"}))

    area = forms.FloatField(
        required=True, label= "Area", min_value=1, 
        widget=forms.NumberInput(attrs={"title":"Ingrese el área en unidades de hectárea","placeholder":"Hectáreas" ,"class": "form-control"}))

class AddLoteForm(forms.ModelForm):
    
    class Meta:
        model = Lote
        fields = [
            'name',
            'tipo',
            'cultivo',
            'variedad',
            'edad',
            'area',
            'finca'
            #'riesgo'
        ]

    name = forms.CharField(
        required=False, label="Nombre",
        widget=forms.TextInput(
        attrs={"title":"Nombre del lote","placeholder":"Nombre" ,"size": 25, "class": "form-control"}))

    tipo = forms.ChoiceField(
        required=False, label="Tipo de cultivo",
        widget=forms.Select(
            attrs={"class": "form-control"}), choices=TIPO_OPTIONS)

    cultivo = forms.ChoiceField(
        required=False, label="Cultivo",
        widget=forms.Select(
            attrs={"class": "form-control"}), choices=CULTIVO_OPTIONS)

    variedad = forms.ChoiceField(
        required=False, label="Variedad",
        widget=forms.Select(
            attrs={"class": "form-control"}), choices=VARIEDAD_OPTIONS)

    edad = forms.FloatField(
        required=False, label= "Edad en años", widget=forms.NumberInput(attrs={"placeholder":"Años < 0: pasado | Años > 0: futuro" 
            ,"title":"Ingrese en años hace cuanto se hizo o se hará la inversión. \n Ejemplo:\n 1)Digite -4 si la inversión fue hecha hace 4 años.\n 2)Digite 6 si la inversión se hará en 6 años.", "class": "form-control"}))

    area = forms.FloatField(
        required=False, label= "Área", min_value=1, 
        widget=forms.NumberInput(attrs={"title":"Ingrese el area en unidades de hectárea","placeholder":"hectáreas" ,"class": "form-control"}))

    finca = forms.ModelChoiceField(queryset = Finca.objects.all(),label = "Pertenece a la finca", 
        widget=forms.Select(attrs={"title":"Seleccione la finca en la que estará este lote.", "class": "form-control"}))

    #riesgo = forms.ModelChoiceField(queryset = Riesgo.objects.all(),label = "Cuales son sus riesgos", widget=forms.Select(attrs={"class": "form-control"}))

class AddRiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = [
            'mercado',
            'fitosanitario',
            'fluctuacion_precio',
            'administracion',
            'tecnologia',
            'mano_de_obra',
            'clima',
            'perecedero',
            'agremiacion',
            'inseguridad'
        ]

    mercado = forms.FloatField(
        required=False, label= "Mercado", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Mercado[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 la probabilidad de que los precios del mercado perjudicen que la inversión a futuro."}))
    fitosanitario = forms.FloatField(
        required=False, label= "Fitosanitario", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Fitosanitario[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 la probabilidad de que insectos, ácaros, moluscos, roedores, hongos, malas hierbas, bacterias y otras formas de vida animal o vegetal puedan perjudidar la inversión."}))
    fluctuacion_precio = forms.FloatField(
        required=False, label= "Fluctuación", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Fluctuación de precio[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 respecto a la oferta y la demanda, la probabilidad de que los precios del cultivo varien con el tiempo."}))
    administracion = forms.FloatField(
        required=False, label= "Administración", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Administración[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 los costos de administración, donde 1 es bajo y 10 es muy alto."}))
    tecnologia = forms.FloatField(
        required=False, label= "Tecnología", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Tecnologia[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 los costos tecnológicos que conlleva la inversión a futuro, donde 1 es bajo y 10 es muy alto."}))
    mano_de_obra = forms.FloatField(
        required=False, label= "Mano de obra", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Mano de obra[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 los costos de mano de obra que conlleva la inversión a futuro, donde 1 es bajo y 10 es muy alto."}))
    clima = forms.FloatField(
        required=False, label= "Clima", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Clima[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 la probabilidad de que el clima no sea favorable para el tipo de cultivo"}))
    perecedero = forms.FloatField(
        required=False, label= "Perecedero", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Perecedero[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 la probabilidad de que el cultivo perezca antes de que de ingresos."}))
    agremiacion = forms.FloatField(
        required=False, label= "Agremiación", min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Agremiación[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 los costos de agremiación que conlleva la inversión a futuro, donde 1 es bajo y 10 es muy alto."}))
    inseguridad = forms.FloatField(
        required=False, label= "Inseguridad", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Inseguridad[0,10]", "class": "form-control",
            "title":"Califique del 1 a 10 la probabilidad de que roben en los cultivos."}))

class AddEstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        fields = [
            'preparacionTerreno',
            'trazo',
            'hoyado',
            'distribucionColino',
            'aplicacionCorrectivos',
            'aplicacionMicorriza',
            'aplicacionMateriaOrganica',
            'siembra',
            'resiembra'
        ]

    preparacionTerreno = forms.FloatField(
        required=True, label= "Preparación de terreno", initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    trazo = forms.FloatField(
        required=True, label= "Trazo", initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    hoyado = forms.FloatField(
        required=True, label= "Hoyado", initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    distribucionColino = forms.FloatField(
        required=True, label= "Distribución de colino",initial = 6666, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    aplicacionCorrectivos = forms.FloatField(
        required=True, label= "Aplicación correctivos",initial = 6666, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    aplicacionMicorriza = forms.FloatField(
        required=True, label= "Aplicación micorriza", initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    aplicacionMateriaOrganica = forms.FloatField(
        required=True, label= "Aplicación de materia organica", initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    siembra = forms.FloatField(
        required=True, label= "Siembra", initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    resiembra = forms.FloatField(
        required=True, label= "Resiembra",initial = 6666,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))

class AddcipcForm(forms.ModelForm):
    class Meta:
        model = CIPC
        fields = [
            'gastosGenerales',
            'prestacionesSociales',
            'impuestoPredial',
            'gastosFinancieros'
        ]

    gastosGenerales = forms.FloatField(
        required=True, label= "Gastos generales", min_value=0,initial = 123, 
        widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    prestacionesSociales = forms.FloatField(
        required=True, label= "Prestaciones sociales", min_value=0,initial = 123, 
        widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    impuestoPredial = forms.FloatField(
        required=True, label= "Impuesto predial", min_value=0,initial = 123, 
        widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    gastosFinancieros = forms.FloatField(
        required=True, label= "Gastos financieros", min_value=0,initial = 123, 
        widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))

class AddData_moForm(forms.ModelForm):
    class Meta:
        model = Data_mo
        fields = [
            'rendimiento',
            'frecuencia',
            'unidad'
        ]

    rendimiento = forms.FloatField(
        required=True, label= "Rendimiento", initial = 123,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"", "class": "form-control"}))
    frecuencia = forms.FloatField(
        required=True, label= "Frecuencia",initial = 123,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"", "class": "form-control"}))
    unidad = forms.FloatField(
        required=True, label= "Unidad", initial = 123,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"jor/dia", "class": "form-control"}))

class AddPreparacion_costosForm(forms.ModelForm):
    class Meta:
        model = Preparacion_costos
        fields = [
            'resiembra',
            'colino',
            'estacas',
            'cal',
            'dap',
            'micorriza',
            'vinilo',
            'paecilomyces',
            'trichoderma',
            'melaza'
        ]

    resiembra = forms.FloatField(
    required=True, label= "Resiembra", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    colino = forms.FloatField(
    required=True, label= "Colino", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    estacas = forms.FloatField(
    required=True, label= "Estacas", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    cal = forms.FloatField(
    required=True, label= "Cal", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    dap = forms.FloatField(
    required=True, label= "Dap", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    micorriza = forms.FloatField(
    required=True, label= "Micorriza", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    vinilo = forms.FloatField(
    required=True, label= "Vinilo", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    paecilomyces = forms.FloatField(
    required=True, label= "Paecilomyces", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    trichoderma = forms.FloatField(
    required=True, label= "Trichoderma", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    melaza = forms.FloatField(
    required=True, label= "Melaza", min_value=0,initial = 4444, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))

class AddCostosForm(forms.ModelForm):
    class Meta:
        model = Costos
        fields = [
            'cantidadSitio',
            'cantidadHectarea',
            'frecuencia'
        ]

    cantidadSitio = forms.FloatField(
    required=True, label= "Cantidad por sitio", min_value=0,initial = 1, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    cantidadHectarea = forms.FloatField(
    required=True, label= "Cantidad por hectárea", min_value=0,initial = 1, 
    widget=forms.NumberInput(attrs={"placeholder":"Hectáreas", "class": "form-control"}))
    frecuencia = forms.FloatField(
    required=True, label= "Frecuencia", min_value=0,initial = 1, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))

class AddDatos_generalesForm(forms.ModelForm):
    class Meta:
        model = Datos_generales
        fields = [
            #"empresa",
            #"departamento",
            #"vereda",
            "gastos_operacionales",
            "valor_de_tierra",
            "densidad",
            "jornal",
            "altitud"
        ]

    gastos_operacionales = forms.FloatField(
    required=True, label= "Gastos operacionales", min_value=0,initial = 3333, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    valor_de_tierra = forms.FloatField(
    required=True, label= "Valor de tierra", min_value=0,initial = 3333, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    densidad = forms.FloatField(
    required=True, label= "Densidad", min_value=0,initial = 3333, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    jornal = forms.FloatField(
    required=True, label= "Jornal", min_value=0,initial = 3333, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
    altitud = forms.FloatField(
    required=True, label= "Altitud", min_value=0,initial = 3333, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))

class AddProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = [
            "ano1",
            "ano2",
            "ano3",
            "ano4",
            "ano5",
            "ano6",
            "ano7",
            "ano8",
            "ano9",
            "ano10",
            "ano11",
            "ano12",
            "ano13",
            "ano14",
            "ano15"
        ]

    ano1 = forms.FloatField(
    required=True, label= "Año 1", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 1", "class": "form-control"}))
    ano2 = forms.FloatField(
    required=True, label= "Año 2", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 2", "class": "form-control"}))
    ano3 = forms.FloatField(
    required=True, label= "Año 3", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 3", "class": "form-control"}))
    ano4 = forms.FloatField(
    required=True, label= "Año 4", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 4", "class": "form-control"}))
    ano5 = forms.FloatField(
    required=True, label= "Año 5", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 5", "class": "form-control"}))
    ano6 = forms.FloatField(
    required=True, label= "Año 6", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 6", "class": "form-control"}))
    ano7 = forms.FloatField(
    required=True, label= "Año 7", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 7", "class": "form-control"}))
    ano8 = forms.FloatField(
    required=True, label= "Año 8", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 8", "class": "form-control"}))
    ano9 = forms.FloatField(
    required=True, label= "Año 9", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 9", "class": "form-control"}))
    ano10 = forms.FloatField(
    required=True, label= "Año 10", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 10", "class": "form-control"}))
    ano11 = forms.FloatField(
    required=True, label= "Año 11", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 11", "class": "form-control"}))
    ano12 = forms.FloatField(
    required=True, label= "Año 12", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 12", "class": "form-control"}))
    ano13 = forms.FloatField(
    required=True, label= "Año 13", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 13", "class": "form-control"}))
    ano14 = forms.FloatField(
    required=True, label= "Año 14", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 14", "class": "form-control"}))
    ano15 = forms.FloatField(
    required=True, label= "Año 15", min_value=0,initial = 9000, 
    widget=forms.NumberInput(attrs={"placeholder":"producción 15", "class": "form-control"}))        

class AddPorcentaje_precioForm(forms.ModelForm):
    class Meta:
        model = Porcentaje_precio
        fields = [
            "precio",
            "porcentaje"
        ]

    precio = forms.FloatField(
    required=True, label= "Precio", min_value=0,initial = 12, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    porcentaje = forms.FloatField(
    required=True, label= "Porcentaje", min_value=0,initial = 12, 
    widget=forms.NumberInput(attrs={"placeholder":"%", "class": "yearsform form-control"}))

class AddInsumos_generalesForm(forms.ModelForm):
    class Meta:
        model = Insumos_generales
        fields = [
            'arbol',
            'fungicida',
            'insecticida',
            'herbicida',
            'canatillas',
            'materiaOrganica',
            'proteina_hidrolizada',
            'coadyuvantes',
            'fertilizante',
            'ridomil'
        ]

    arbol = forms.FloatField(
    required=True, label= "Arbol", min_value=0,initial = 2222,
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    fungicida = forms.FloatField(
    required=True, label= "Fungicida", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    insecticida = forms.FloatField(
    required=True, label= "Insecticida", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    herbicida = forms.FloatField(
    required=True, label= "Herbicida", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    canatillas = forms.FloatField(
    required=True, label= "Canatillas", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    materiaOrganica = forms.FloatField(
    required=True, label= "Materia organica", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    proteina_hidrolizada = forms.FloatField(
    required=True, label= "Proteina hidrolizada", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    coadyuvantes = forms.FloatField(
    required=True, label= "coadyuvante", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    fertilizante = forms.FloatField(
    required=True, label= "fertilizante", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    ridomil = forms.FloatField(
    required=True, label= "ridomil", min_value=0,initial = 2222, 
    widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))

class AddBase_presupuestalForm(forms.ModelForm):
    class Meta:
        model = Base_presupuestal
        fields = [
            'tipo',
            'cultivo',
            'variedad',
            'nombre'
            #'rentabilidad',
            #'datos_g',
            #'insumos_g',
            #'preparacion',
            #'costos_insumos',
            #'insumos_mo',
            #'distribucion_calidad',
            #'establecimiento_r',
            #'cipc'
        ]

    tipo = forms.ChoiceField(
        required=True, label="Tipo", widget=forms.Select(attrs={"class": "form-control"}), choices=TIPO_OPTIONS)

    cultivo = forms.ChoiceField(
        required=True, label="Cultivo", widget=forms.Select(attrs={"class": "form-control"}), choices=CULTIVO_OPTIONS)

    variedad = forms.ChoiceField(
        required=True, label="Variedad", widget=forms.Select(attrs={"class": "form-control"}), choices=VARIEDAD_OPTIONS)

    nombre = forms.CharField(
        required=True, label="Nombre",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre", "class": "form-control"}))

class EditUserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "document_type",
            "document_number",
            "first_name",
            "last_name",
            "address",
            "phone",
            "email",
            "birthdate",
            "gender",
            "password",
        ]

    document_type = forms.ChoiceField(
        required=True, widget=forms.RadioSelect, choices=DOCUMENT_OPTIONS)
    document_number = forms.CharField(
        required=True, label="Número de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Número de documento"}))
    first_name = forms.CharField(
        required=True, label="Primer Nombre",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre"}))
    last_name = forms.CharField(
        required=True, label="Apellido",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Apellido"}))
    address = forms.CharField(
        required=True, label="Dirección de Residencia",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Dirección de Residencia"}))
    birthdate = forms.DateField(
        required=True, label="Fecha de nacimiento",
        input_formats=["%Y-%m-%d",
                       "%d/%m/%Y",
                       "%d/%m/%y"], widget=forms.TextInput(attrs={"class": "form-control"})
    )
    gender = forms.ChoiceField(
        required=True, widget=forms.Select(attrs={"class": "form-control"}), choices=GENDER_OPTIONS)
    phone = forms.CharField(
        required=True, label="Número de teléfono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de telefono"}))
    email = forms.EmailField(
        required=True, label="Email", widget=forms.TextInput())
    password = forms.CharField(
        required=True, label="Password", widget=forms.PasswordInput())

class EditBase_presupuestalForm(forms.ModelForm):
    class Meta:
        model = Base_presupuestal
        fields = [
            'tipo',
            'cultivo',
            'variedad',
            'nombre',
            'rentabilidad',
            'datos_g',
            'insumos_g',
            'preparacion',
            'costos_insumos',
            'insumos_mo',
            'distribucion_calidad',
            'establecimiento_r',
            'cipc'
        ]

    tipo = forms.ChoiceField(
        required=True, label="Tipo", widget=forms.Select(attrs={"class": "form-control"}), choices=TIPO_OPTIONS)

    cultivo = forms.ChoiceField(
        required=True, label="Cultivo", widget=forms.Select(attrs={"class": "form-control"}), choices=CULTIVO_OPTIONS)

    variedad = forms.ChoiceField(
        required=True, label="Variedad", widget=forms.Select(attrs={"class": "form-control"}), choices=VARIEDAD_OPTIONS)

    nombre = forms.CharField(
        required=True, label="Nombre",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre", "class": "form-control"}))

    rentabilidad = forms.FloatField(
        required=True, label= "rentabilidad", min_value=0,initial = 12, 
        widget=forms.NumberInput(attrs={"placeholder":"$", "class": "yearsform form-control"}))
    datos_g = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Datos_generales.objects.all())
    insumos_g = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Insumos_generales.objects.all())
    preparacion = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Preparacion_costos.objects.all())
    costos_insumos = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Costos_insumos.objects.all())
    insumos_mo = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Insumos_mo.objects.all())
    distribucion_calidad = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Distribucion_calidad.objects.all())
    establecimiento_r = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Establecimiento.objects.all())
    cipc = forms.ModelChoiceField(
        required=True, label="Género", widget=forms.Select(attrs={"class": "form-control"}), queryset = Ano_cipc.objects.all())

class chooseBD(forms.Form):
    bp = forms.ModelChoiceField(queryset = Base_presupuestal.objects.all(),label = "Elige la base presupuestal ", 
        widget=forms.Select(attrs={"title":"Seleccione la base presupuestal.", "class": "form-control"}))