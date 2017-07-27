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
        required=True, label="Numero de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Numero de documento", "class": "form-control"}))

    document_type = forms.ChoiceField(
        required=True, label= "Tipo de documento", widget=forms.RadioSelect(attrs={"title": "Tipo de documento","class": "radio-inline"}), choices=DOCUMENT_OPTIONS)

    gender = forms.ChoiceField(
        required=True, label="Genero", widget=forms.Select(attrs={"class": "form-control"}), choices=GENDER_OPTIONS)

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
        required=True, label="Direccion de Residencia",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Direccion de Residencia", "class": "form-control"}
        ))
    phone = forms.CharField(
        required=True, label="Numero de telefono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Numero de telefono", "class": "form-control"}
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
            'finca',
            'riesgo'
        ]

    name = forms.CharField(
        required=True, label="Nombre del lote",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control"}))

    tipo = forms.CharField(
        required=True, label="Tipo",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control"}))

    cultivo = forms.CharField(
        required=True, label="Cultivo",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control"}))

    variedad = forms.CharField(
        required=True, label="Variedad",
        widget=forms.TextInput(
            attrs={"size": 25, "class": "form-control"}))

    edad = forms.FloatField(
        required=True, label= "Edad", min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))

    area = forms.FloatField(
        required=True, label= "Area", min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))

    finca = forms.ModelChoiceField(queryset = Finca.objects.all(),label = "Pertenece a la finca", widget=forms.Select(attrs={"class": "form-control"}))

    riesgo = forms.ModelChoiceField(queryset = Riesgo.objects.all(),label = "Cuales son sus riesgos", widget=forms.Select(attrs={"class": "form-control"}))

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


class AddInsumos_generalesForm(forms.ModelForm):
    class Meta:
        model = Insumos_generales
        fields = [
            'arbol',
            'fungicida',
            'insecticida',
            'herbicida',
            'canatillas',
            'proteina_hidrolizada',
            'coadyuvantes'
        ]

class AddPorcentaje_precioForm(forms.ModelForm):
    class Meta:
        model = Porcentaje_precio
        fields = [
            'precio',
            'porcentaje'
        ]

class AddDistribucion_calidadForm(forms.ModelForm):
    class Meta:
        model = Distribucion_calidad
        fields = [
            'primera',
            'segunda',
            'tercera',
            'produccion'
        ]

class AddDatos_generalesForm(forms.ModelForm):
    class Meta:
        model = Datos_generales
        fields = [
            'empresa',
            'departamento',
            'vereda',
            'gastos_operacionales',
            'valor_de_tierra',
            'densidad',
            'jornal',
            'altitud'
        ]


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
        required=True, label="Numero de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Numero de documento"}))
    first_name = forms.CharField(
        required=True, label="Primer Nombre",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre"}))
    last_name = forms.CharField(
        required=True, label="Apellido",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Apellido"}))
    address = forms.CharField(
        required=True, label="Direccion de Residencia",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Direccion de Residencia"}))
    birthdate = forms.DateField(
        required=True, label="Fecha de nacimiento",
        input_formats=["%Y-%m-%d",
                       "%d/%m/%Y",
                       "%d/%m/%y"], widget=forms.TextInput(attrs={"class": "form-control"})
    )
    gender = forms.ChoiceField(
        required=True, widget=forms.Select(attrs={"class": "form-control"}), choices=GENDER_OPTIONS)
    phone = forms.CharField(
        required=True, label="Numero de telefono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Numero de telefono"}))
    email = forms.EmailField(
        required=True, label="Email", widget=forms.TextInput())
    password = forms.CharField(
        required=True, label="Password", widget=forms.PasswordInput())