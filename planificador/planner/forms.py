# -*- coding: utf-8 -*-
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
                       "%d/%m/%y"], widget=forms.TextInput(attrs={"class": "form-control"})
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
        required=True, label="Email", widget=forms.TextInput(attrs={"class": "form-control"}))
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
        required=True, label="Nombre de la finca",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control"}))

    area = forms.FloatField(
        required=True, label= "Area", min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))

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
        required=True, label="Nombre del lote",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control"}))

    tipo = forms.ChoiceField(
        required=True, label="Tipo",
        widget=forms.Select(
            attrs={"class": "form-control"}), choices=TIPO_OPTIONS)

    cultivo = forms.ChoiceField(
        required=True, label="Cultivo",
        widget=forms.Select(
            attrs={"class": "form-control"}), choices=CULTIVO_OPTIONS)

    variedad = forms.ChoiceField(
        required=True, label="Variedad",
        widget=forms.Select(
            attrs={"class": "form-control"}), choices=VARIEDAD_OPTIONS)

    edad = forms.FloatField(
        required=True, label= "Edad", widget=forms.NumberInput(attrs={"class": "form-control"}))

    area = forms.FloatField(
        required=True, label= "Area", min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))

    finca = forms.ModelChoiceField(queryset = Finca.objects.all(),label = "Pertenece a la finca", widget=forms.Select(attrs={"class": "form-control"}))

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
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Mercado[0,10]", "class": "riesgoform form-control"}))
    fitosanitario = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Fitosanitario[0,10]", "class": "riesgoform form-control"}))
    fluctuacion_precio = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Fluctuacion de precio[0,10]", "class": "riesgoform form-control"}))
    administracion = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Administracion[0,10]", "class": "riesgoform form-control"}))
    tecnologia = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Tecnologia[0,10]", "class": "riesgoform form-control"}))
    mano_de_obra = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Mano de obra[0,10]", "class": "riesgoform form-control"}))
    clima = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Clima[0,10]", "class": "riesgoform form-control"}))
    perecedero = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Perecedero[0,10]", "class": "riesgoform form-control"}))
    agremiacion = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Agremiacion[0,10]", "class": "riesgoform form-control"}))
    inseguridad = forms.FloatField(
        required=True, label= "", min_value=0, max_value=10, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"Inseguridad[0,10]", "class": "riesgoform form-control"}))

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
        required=True, label= "Preparacion de terreno", initial = 6666,
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
        required=True, label= "Aplicacion correctivos",initial = 6666, 
        widget=forms.NumberInput(attrs={"size":10, "placeholder":"$", "class": "form-control"}))
    aplicacionMicorriza = forms.FloatField(
        required=True, label= "Aplicacion micorriza", initial = 6666,
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
    required=True, label= "Cantidad por hectarea", min_value=0,initial = 1, 
    widget=forms.NumberInput(attrs={"placeholder":"#", "class": "form-control"}))
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
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 1", "class": "produccionform form-control"}))
    ano2 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 2", "class": "produccionform form-control"}))
    ano3 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 3", "class": "produccionform form-control"}))
    ano4 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 4", "class": "produccionform form-control"}))
    ano5 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 5", "class": "produccionform form-control"}))
    ano6 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 6", "class": "produccionform form-control"}))
    ano7 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 7", "class": "produccionform form-control"}))
    ano8 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 8", "class": "produccionform form-control"}))
    ano9 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 9", "class": "produccionform form-control"}))
    ano10 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 10", "class": "produccionform form-control"}))
    ano11 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 11", "class": "produccionform form-control"}))
    ano12 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 12", "class": "produccionform form-control"}))
    ano13 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 13", "class": "produccionform form-control"}))
    ano14 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 14", "class": "produccionform form-control"}))
    ano15 = forms.FloatField(
    required=True, label= "", min_value=0,initial = 1111, 
    widget=forms.NumberInput(attrs={"placeholder":"produccion 15", "class": "produccionform form-control"}))        

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