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
            "phone",
            "role",
            "is_active"
        ]

    document_number = forms.CharField(
        required=True, label="Numero de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Numero de documento", "class": "form-control"}))

    document_type = forms.ChoiceField(
        required=True, label= "Tipo de documento", widget=forms.RadioSelect(attrs={"title": "Tipo de documento","class": "radio-inline"}), choices=DOCUMENT_OPTIONS)

    gender = forms.ChoiceField(
        required=True, widget=forms.Select(attrs={"class": "form-control"}), choices=GENDER_OPTIONS)

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

    role = forms.ChoiceField(
        required=True, widget=forms.Select(attrs={"class": "form-control"}), choices=ROLE_OPTIONS)

    is_active = forms.BooleanField(required=True)


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
        fields = ['name', 'area', 'agricultor']

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

class AddLoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = [
            'tipo',
            'cultivo',
            'variedad',
            'edad',
            'area',
            'finca',
            'riesgo'
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