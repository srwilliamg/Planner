# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
from .auth import UserManager
from django.utils.translation import gettext as _


ROLE_OPTIONS = (("R", "Root"), ("A", "Administrador"),("S", "Agricultor"))
DOCUMENT_OPTIONS = (("TI", "Tarjeta de Identidad"), ("CC", "Cedula de Ciudadania"), ("CE", "Cedula de Extranjería"))
GENDER_OPTIONS = (("M", "Masculino"), ("F", "Femenino"), ("O", "Other"))


class User(AbstractBaseUser):
    document_type = models.CharField(max_length=5, choices=DOCUMENT_OPTIONS, default="CC")
    document_number = models.CharField(max_length=30)

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    birthdate = models.DateField(null=True, blank=False)
    gender = models.CharField(max_length=2, choices=GENDER_OPTIONS)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

    role = models.CharField(max_length=1, choices=ROLE_OPTIONS,
                            null=False, blank=False)

    is_active = models.BooleanField(default=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(_('last_login'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = [USERNAME_FIELD, "password"]

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def is_staff(self):
        return self.role == "R"

    def has_perm(self, perm, obj=None):
        return self.role == "R"

    def has_module_perms(self, package_name):
        return self.role == "R"

    def __str__(self):
        return u"{} {} [{}]".format(self.first_name, self.last_name,
                                    self.email)

    __unicode__ = __str__

class Finca(models.Model):
    name = models.CharField(max_length=150, default="FincaVerde")
    area = models.FloatField(default=32000)
    agricultor = models.ForeignKey(User, blank=False,related_name= "finca_agricultor")

    def __str__(self):
        return u"{} {}".format(self.name, self.area)

    def getValues(self):
        return {"nombre":self.name, "area":self.area, "agricultor": self.agricultor.getValues()}

class Riesgo(models.Model):
    mercado = models.FloatField(default=1)
    fitosanitario = models.FloatField(default=1)
    fluctuacion_precio = models.FloatField(default=1)
    administracion = models.FloatField(default=1)
    tecnologia = models.FloatField(default=1)
    mano_de_obra = models.FloatField(default=1)
    clima = models.FloatField(default=1)
    perecedero = models.FloatField(default=1)
    agremiacion = models.FloatField(default=1)
    inseguridad = models.FloatField(default=1)

    def getValues(self):
        return {"mercado":self.mercado, "fitosanitario":self.fitosanitario, "fluctuacion_precio":self.fluctuacion_precio, 
        "administracion":self.administracion,"tecnologia":self.tecnologia, "mano_de_obra":self.mano_de_obra, "cliam":self.clima, "perecedero":self.perecedero,
        "agremiacion":self.agremiacion, "inseguridad":self.inseguridad}

class Lote(models.Model):
    name = models.CharField(max_length=150, null=False, default="Lote")
    tipo = models.CharField(max_length=150, default="Verde")
    cultivo = models.CharField(max_length=150, default="Verde")
    variedad = models.CharField(max_length=150, default="Verde")
    edad = models.FloatField(default=3)
    area = models.FloatField(default=4000)
    finca = models.ForeignKey(Finca, blank=False,related_name= "lote_finca")
    riesgo = models.OneToOneField(Riesgo, related_name= "lote_riesgo")

    def __str__(self):
        return u"{} {} {}".format(self.tipo, self.cultivo, self.variedad)

    def getValues(self):
        return {
        "name": self.name,
        "tipo": self.tipo,
        "cultivo": self.cultivo,
        "variedad": self.variedad,
        "edad": self.edad,
        "area": self.area,
        "finca": self.finca,
        "riesgo": self.riesgo
        }

class Insumos_generales(models.Model):
    arbol = models.FloatField(default=400)
    fungicida = models.FloatField(default=400)
    insecticida = models.FloatField(default=400)
    herbicida = models.FloatField(default=400)
    canatillas = models.FloatField(default=400)
    materiaOrganica = models.FloatField(default=400)
    proteina_hidrolizada = models.FloatField(default=400)
    coadyuvantes = models.FloatField(default=400)
    fertilizante = models.FloatField(default=400)
    ridomil = models.FloatField(default=400)

    def getValues(self):
        return {
            "arbol": self.arbol,
            "fungicida": self.fungicida,
            "insecticida": self.insecticida,
            "herbicida": self.herbicida,
            "canatillas": self.canatillas,
            "materiaOrganica":self.materiaOrganica,
            "proteina_hidrolizada": self.proteina_hidrolizada,
            "coadyuvantes": self.coadyuvantes,
            "fertilizante": self.fertilizante,
            "ridomil": self.ridomil
        }

class Porcentaje_precio(models.Model):
    precio = models.FloatField()
    porcentaje = models.FloatField()

    def __str__(self):
        return u"{}$-{}%".format(self.precio, self.porcentaje)

    def mult(self):
        return self.precio*(self.porcentaje/100)

    def getValues(self):
        return {"precio":self.precio, "porcentaje":self.porcentaje, "mult": self.mult()}

class Produccion(models.Model):
    ano1 = models.FloatField(default=120)
    ano2 = models.FloatField(default=120)
    ano3 = models.FloatField(default=120)
    ano4 = models.FloatField(default=120)
    ano5 = models.FloatField(default=120)
    ano6 = models.FloatField(default=120)
    ano7 = models.FloatField(default=120)
    ano8 = models.FloatField(default=120)
    ano9 = models.FloatField(default=120)
    ano10 = models.FloatField(default=120)
    ano11 = models.FloatField(default=120)
    ano12 = models.FloatField(default=120)
    ano13 = models.FloatField(default=120)
    ano14 = models.FloatField(default=120)
    ano15 = models.FloatField(default=120)

    def getValues(self):
        return {
        "ano1": self.ano1,
        "ano2": self.ano2,
        "ano3": self.ano3,
        "ano4": self.ano4,
        "ano5": self.ano5,
        "ano6": self.ano6,
        "ano7": self.ano7,
        "ano8": self.ano8,
        "ano9": self.ano9,
        "ano10": self.ano10,
        "ano11": self.ano11,
        "ano12": self.ano12,
        "ano13": self.ano13,
        "ano14": self.ano14,
        "ano15": self.ano15
        }

class Distribucion_calidad(models.Model):
    primera = models.OneToOneField(Porcentaje_precio, related_name= "dc_primera")
    segunda = models.OneToOneField(Porcentaje_precio, related_name= "dc_segunda")
    tercera = models.OneToOneField(Porcentaje_precio, related_name= "dc_tercera")
    produccion = models.OneToOneField(Produccion, related_name="dc_produccion")

    def getValues(self):
        return {"primera":self.primera.getValues(), "segunda":self.primera.getValues(),
                "tercera": self.primera.getValues(),"produccion":self.produccion.getValues().values()}

class Datos_generales(models.Model):
    empresa = models.CharField(max_length= 125, default="empresa")
    departamento = models.CharField(max_length= 125, default="Risaralda")
    vereda = models.CharField(max_length= 125, default="El cedral")
    gastos_operacionales = models.FloatField(default=300)
    valor_de_tierra = models.FloatField(default=400)
    densidad = models.FloatField(default=400)
    jornal = models.FloatField(default=3000)
    altitud = models.FloatField(default=1000)

    def getValues(self):
        return{
            "empresa":self.empresa,
            "departamento":self.departamento,
            "vereda":self.vereda,
            "gastos_operacionales":self.gastos_operacionales,
            "valor_de_tierra":self.valor_de_tierra,
            "densidad":self.densidad,
            "jornal":self.jornal,
            "altitud":self.altitud
        }

class Costos(models.Model):
    cantidadSitio = models.FloatField(default= 2)
    cantidadHectarea = models.FloatField(default= 4)
    frecuencia = models.FloatField(default=1)

    def getValues(self):
        return {"cantidadH":self.cantidadHectarea, "cantidadS":self.cantidadSitio, "frecuencia": self.frecuencia}
    
class Preparacion_costos(models.Model):
    resiembra = models.OneToOneField(Costos, related_name="resiembra_costos")
    colino = models.OneToOneField(Costos, related_name="colino_costos")
    estacas = models.OneToOneField(Costos, related_name="estacas_costos")
    cal = models.OneToOneField(Costos, related_name="cal_costos")
    dap = models.OneToOneField(Costos, related_name="dap_costos")
    micorriza = models.OneToOneField(Costos, related_name="micorriza_costos")
    vinilo = models.OneToOneField(Costos, related_name="vinilo_costos")
    paecilomyces = models.OneToOneField(Costos, related_name="paecilomyces_costos")
    trichoderma = models.OneToOneField(Costos, related_name="trichoderma_costos")
    melaza = models.OneToOneField(Costos, related_name="melaza_costos")

    def getValues(self):
        return {
            "colino": self.colino.getValues(),
            "estacas": self.estacas.getValues(),
            "cal": self.cal.getValues(),
            "dap": self.dap.getValues(),
            "micorriza": self.micorriza.getValues(),
            "vinilo": self.vinilo.getValues(),
            "paecilomyces": self.paecilomyces.getValues(),
            "trichoderma": self.trichoderma.getValues(),
            "melaza": self.melaza.getValues(),
        }

class Ano_costo(models.Model):
    ano1 = models.OneToOneField(Costos, related_name= "ano1_datamo")
    ano2 = models.OneToOneField(Costos, related_name= "ano2_datamo")
    ano3 = models.OneToOneField(Costos, related_name= "ano3_datamo")
    ano4 = models.OneToOneField(Costos, related_name= "ano4_datamo")
    ano5 = models.OneToOneField(Costos, related_name= "ano5_datamo")
    ano6 = models.OneToOneField(Costos, related_name= "ano6_datamo")
    ano7 = models.OneToOneField(Costos, related_name= "ano7_datamo")
    ano8 = models.OneToOneField(Costos, related_name= "ano8_datamo")
    ano9 = models.OneToOneField(Costos, related_name= "ano9_datamo")
    ano10 = models.OneToOneField(Costos, related_name= "ano10_datamo")
    ano11 = models.OneToOneField(Costos, related_name= "ano11_datamo")
    ano12 = models.OneToOneField(Costos, related_name= "ano12_datamo")
    ano13 = models.OneToOneField(Costos, related_name= "ano13_datamo")
    ano14 = models.OneToOneField(Costos, related_name= "ano14_datamo")
    ano15 = models.OneToOneField(Costos, related_name= "ano15_datamo")

    def getValues(self):
        return {
            "ano1": self.ano1.getValues(),
            "ano2": self.ano2.getValues(),
            "ano3": self.ano3.getValues(),
            "ano4": self.ano4.getValues(),
            "ano5": self.ano5.getValues(),
            "ano6": self.ano6.getValues(),
            "ano7": self.ano7.getValues(),
            "ano8": self.ano8.getValues(),
            "ano9": self.ano9.getValues(),
            "ano10": self.ano10.getValues(),
            "ano11": self.ano11.getValues(),
            "ano12": self.ano12.getValues(),
            "ano13": self.ano13.getValues(),
            "ano14": self.ano14.getValues(),
            "ano15": self.ano15.getValues()
        }

class Costos_insumos(models.Model):
    materiaOrganica = models.OneToOneField(Ano_costo, related_name="materiaOrganica_anocosto")
    herbicidaCalles = models.OneToOneField(Ano_costo, related_name="herbicidaCalles_anocosto")
    herbicidaPlatos = models.OneToOneField(Ano_costo, related_name="herbicidaPlatos_anocosto")
    insecticidas = models.OneToOneField(Ano_costo, related_name="insecticidas_anocosto")
    fungicidas = models.OneToOneField(Ano_costo, related_name="fungicidas_anocosto")
    fertilizante = models.OneToOneField(Ano_costo, related_name="fertilizante_anocosto")
    ridomil = models.OneToOneField(Ano_costo, related_name="ridomil_anocosto")
    fertilizanteFoliar = models.OneToOneField(Ano_costo, related_name="fertilizanteFoliar_anocosto")
    biocontroladores = models.OneToOneField(Ano_costo, related_name="biocontroladores_anocosto")
    guadana = models.OneToOneField(Ano_costo, related_name="guadana_anocosto")
    selectores = models.OneToOneField(Ano_costo, related_name="selectores_anocosto")
    bombasEspalda = models.OneToOneField(Ano_costo, related_name="bombasEspalda_anocosto")
    bombasEstacionarias = models.OneToOneField(Ano_costo, related_name="bombasEstacionarias_anocosto")
    canastillas = models.OneToOneField(Ano_costo, related_name="canastillas_anocosto")
    herramientas = models.OneToOneField(Ano_costo, related_name="herramientas_anocosto")
    lycra = models.OneToOneField(Ano_costo, related_name="lycra_anocosto")

    def getValues(self):
        return {
            "materiaOrganica" : self.materiaOrganica.getValues().values(),
            "herbicidaCalles" : self.herbicidaCalles.getValues().values(),
            "herbicidaPlatos" : self.herbicidaPlatos.getValues().values(),
            "insecticidas" : self.insecticidas.getValues().values(),
            "fungicidas" : self.fungicidas.getValues().values(),
            "fertilizante" : self.fertilizante.getValues().values(),
            "ridomil" : self.ridomil.getValues().values(),
            "fertilizanteFoliar" : self.fertilizanteFoliar.getValues().values(),
            "biocontroladores" : self.biocontroladores.getValues().values(),
            "guadana" : self.guadana.getValues().values(),
            "selectores" : self.selectores.getValues().values(),
            "bombasEspalda" : self.bombasEspalda.getValues().values(),
            "bombasEstacionarias" : self.bombasEstacionarias.getValues().values(),
            "canastillas" : self.canastillas.getValues().values(),
            "herramientas" : self.herramientas.getValues().values(),
            "lycra" : self.lycra.getValues().values()
        }

class Data_mo(models.Model):

    rendimiento = models.FloatField(default=30)
    frecuencia = models.FloatField(default=3)
    unidad = models.CharField(max_length=125, default="jor/dia")

    def __str__(self):
        return u"{} {} {}".format(self.rendimiento, self.frecuencia, self.unidad)

    def getValues(self):
        return {"rendimiento":self.rendimiento, "frecuencia":self.frecuencia, "unidad":self.unidad}

class Anos_mo(models.Model):
    ano1 = models.OneToOneField(Data_mo, related_name= "ano1_datamo")
    ano2 = models.OneToOneField(Data_mo, related_name= "ano2_datamo")
    ano3 = models.OneToOneField(Data_mo, related_name= "ano3_datamo")
    ano4 = models.OneToOneField(Data_mo, related_name= "ano4_datamo")
    ano5 = models.OneToOneField(Data_mo, related_name= "ano5_datamo")
    ano6 = models.OneToOneField(Data_mo, related_name= "ano6_datamo")
    ano7 = models.OneToOneField(Data_mo, related_name= "ano7_datamo")
    ano8 = models.OneToOneField(Data_mo, related_name= "ano8_datamo")
    ano9 = models.OneToOneField(Data_mo, related_name= "ano9_datamo")
    ano10 = models.OneToOneField(Data_mo, related_name= "ano10_datamo")
    ano11 = models.OneToOneField(Data_mo, related_name= "ano11_datamo")
    ano12 = models.OneToOneField(Data_mo, related_name= "ano12_datamo")
    ano13 = models.OneToOneField(Data_mo, related_name= "ano13_datamo")
    ano14 = models.OneToOneField(Data_mo, related_name= "ano14_datamo")
    ano15 = models.OneToOneField(Data_mo, related_name= "ano15_datamo")

    def getValues(self):
        return {
        "ano1": self.ano1.getValues(),
        "ano2": self.ano2.getValues(),
        "ano3": self.ano3.getValues(),
        "ano4": self.ano4.getValues(),
        "ano5": self.ano5.getValues(),
        "ano6": self.ano6.getValues(),
        "ano7": self.ano7.getValues(),
        "ano8": self.ano8.getValues(),
        "ano9": self.ano9.getValues(),
        "ano10": self.ano10.getValues(),
        "ano11": self.ano11.getValues(),
        "ano12": self.ano12.getValues(),
        "ano13": self.ano13.getValues(),
        "ano14": self.ano14.getValues(),
        "ano15": self.ano15.getValues()
        }

class Insumos_mo(models.Model):
    siembra = models.OneToOneField(Anos_mo,related_name= "siembra_anosmo")
    resiembra = models.OneToOneField(Anos_mo,related_name= "resiembra_anosmo")
    limpiaGuadanaCalles = models.OneToOneField(Anos_mo,related_name= "limpiaGuadanacalles_anosmo")
    aplicacionHerbicida = models.OneToOneField(Anos_mo,related_name= "aplicacionHerbicida_anosmo")
    plateo = models.OneToOneField(Anos_mo,related_name= "plateo_anosmo")
    fertilizacion = models.OneToOneField(Anos_mo,related_name= "fertilizacion_anosmo")
    aplicacionMateriaOrganica = models.OneToOneField(Anos_mo,related_name= "aplicacionMateriaOrganica_anosmo")
    fungicidas = models.OneToOneField(Anos_mo,related_name= "fungicidas_anosmo")
    biocontroladores = models.OneToOneField(Anos_mo,related_name= "biocontroladores_anosmo")
    aspersiones = models.OneToOneField(Anos_mo,related_name= "aspersiones_anosmo")
    tutorado = models.OneToOneField(Anos_mo,related_name= "tutorado_anosmo")
    podas = models.OneToOneField(Anos_mo,related_name= "podas_anosmo")
    recoleccionContrato = models.OneToOneField(Anos_mo,related_name= "recoleccionContrato_anosmo")
    recoleccionDia = models.OneToOneField(Anos_mo,related_name= "recoleccionDia_anosmo")

    def getValues(self):
        return {
            "siembra" : self.siembra.getValues().values(),
            "resiembra" : self.resiembra.getValues().values(),
            "limpiaGuadanaCalles" : self.limpiaGuadanaCalles.getValues().values(),
            "aplicacionHerbicida" : self.aplicacionHerbicida.getValues().values(),
            "plateo" : self.plateo.getValues().values(),
            "fertilizacion" : self.fertilizacion.getValues().values(),
            "aplicacionMateriaOrganica" : self.aplicacionMateriaOrganica.getValues().values(),
            "fungicidas" : self.fungicidas.getValues().values(),
            "biocontroladores" : self.biocontroladores.getValues().values(),
            "aspersiones" : self.aspersiones.getValues().values(),
            "tutorado" : self.tutorado.getValues().values(),
            "podas" : self.podas.getValues().values(),
            "recoleccionContrato" : self.recoleccionContrato.getValues().values(),
            "recoleccionDia" : self.recoleccionDia.getValues().values()
        }

class CIPC(models.Model):

    gastosGenerales = models.FloatField(default=100)
    prestacionesSociales = models.FloatField(default=200)
    impuestoPredial = models.FloatField(default=3000)
    gastosFinancieros = models.FloatField(default=200)

    def __str__(self):
        return u"{} {}".format(self.gastosGenerales, self.prestacionesSociales)

    def getValues(self):
        return {
            "gastosGenerales":self.gastosGenerales,
            "prestacionesSociales":self.prestacionesSociales,
            "impuestoPredial":self.impuestoPredial,
            "gastosFinancieros":self.gastosFinancieros
        }

    def getSum(self):
        return self.gastosGenerales + self.prestacionesSociales + self.impuestoPredial + self.gastosFinancieros
        
class Ano_cipc(models.Model):
    ano1 = models.OneToOneField(CIPC, related_name= "ano1_datamo")
    ano2 = models.OneToOneField(CIPC, related_name= "ano2_datamo")
    ano3 = models.OneToOneField(CIPC, related_name= "ano3_datamo")
    ano4 = models.OneToOneField(CIPC, related_name= "ano4_datamo")
    ano5 = models.OneToOneField(CIPC, related_name= "ano5_datamo")
    ano6 = models.OneToOneField(CIPC, related_name= "ano6_datamo")
    ano7 = models.OneToOneField(CIPC, related_name= "ano7_datamo")
    ano8 = models.OneToOneField(CIPC, related_name= "ano8_datamo")
    ano9 = models.OneToOneField(CIPC, related_name= "ano9_datamo")
    ano10 = models.OneToOneField(CIPC, related_name= "ano10_datamo")
    ano11 = models.OneToOneField(CIPC, related_name= "ano11_datamo")
    ano12 = models.OneToOneField(CIPC, related_name= "ano12_datamo")
    ano13 = models.OneToOneField(CIPC, related_name= "ano13_datamo")
    ano14 = models.OneToOneField(CIPC, related_name= "ano14_datamo")
    ano15 = models.OneToOneField(CIPC, related_name= "ano15_datamo")

    def getValues(self):
        return [
            self.ano1.getValues(),
            self.ano2.getValues(),
            self.ano3.getValues(),
            self.ano4.getValues(),
            self.ano5.getValues(),
            self.ano6.getValues(),
            self.ano7.getValues(),
            self.ano8.getValues(),
            self.ano9.getValues(),
            self.ano10.getValues(),
            self.ano11.getValues(),
            self.ano12.getValues(),
            self.ano13.getValues(),
            self.ano14.getValues(),
            self.ano15.getValues()
        ]

    def getSums(self):
        return [
            self.ano1.getSum(),
            self.ano2.getSum(),
            self.ano3.getSum(),
            self.ano4.getSum(),
            self.ano5.getSum(),
            self.ano6.getSum(),
            self.ano7.getSum(),
            self.ano8.getSum(),
            self.ano9.getSum(),
            self.ano10.getSum(),
            self.ano11.getSum(),
            self.ano12.getSum(),
            self.ano13.getSum(),
            self.ano14.getSum(),
            self.ano15.getSum()
        ]
   
class Establecimiento(models.Model):
    preparacionTerreno = models.FloatField(default=200)
    trazo = models.FloatField(default=200)
    hoyado = models.FloatField(default=100)
    distribucionColino = models.FloatField(default=342)
    aplicacionCorrectivos = models.FloatField(default=232)
    aplicacionMicorriza = models.FloatField(default=700)
    aplicacionMateriaOrganica = models.FloatField(default=102)
    siembra = models.FloatField(default=200)
    resiembra = models.FloatField(default=300)

    def getValues(self):
        return {
            "preparacionTerreno":self.preparacionTerreno,
            "trazo":self.trazo,
            "hoyado":self.hoyado,
            "distribucionColino":self.distribucionColino,
            "aplicacionCorrectivos":self.aplicacionCorrectivos,
            "aplicacionMicorriza":self.aplicacionMicorriza,
            "aplicacionMateriaOrganica":self.aplicacionMateriaOrganica,
            "siembra":self.siembra,
            "resiembra":self.resiembra
        }

class Base_presupuestal(models.Model):
    nombre = models.CharField(max_length=125, null=False, default="bp")
    rentabilidad = models.FloatField(default=0)
    datos_g = models.OneToOneField(Datos_generales,related_name="bp_dg")
    insumos_g = models.OneToOneField(Insumos_generales,related_name="bp_ig")
    preparacion = models.OneToOneField(Preparacion_costos,related_name="bp_preparacion")
    costos_insumos = models.OneToOneField(Costos_insumos,related_name="bp_Costosinsumos")
    insumos_mo = models.OneToOneField(Insumos_mo,related_name="bp_insumosmo")
    distribucion_calidad = models.OneToOneField(Distribucion_calidad,related_name="bp_dc")
    establecimiento_r = models.OneToOneField(Establecimiento,related_name="bp_establecimiento", default=1)
    cipc = models.OneToOneField(Ano_cipc, related_name = "bp_cipc")

    def __str__(self):
        return u"{} {}".format(self.nombre, self.rentabilidad)

    def totalInsumos(self):
    # Variables
        dc_produccion = self.distribucion_calidad.getValues()
        datos_g = self.datos_g.getValues()
        costos_insumos = self.costos_insumos.getValues()
        preparacion = self.preparacion.getValues()
    #
        colino = (preparacion["colino"]["cantidadS"]*datos_g["densidad"]) + (preparacion["colino"]["cantidadH"]*datos_g["densidad"]/100)
        pmo_costo = {
            "colino" : colino, #
            "estacas" :(preparacion["estacas"]["cantidadS"]*datos_g["densidad"]),#
            "cal" :(preparacion["cal"]["cantidadS"]*datos_g["densidad"]/1000), #
            "dap" :(preparacion["dap"]["cantidadS"]*datos_g["densidad"]/1000), #
            "micorriza" :(preparacion["micorriza"]["cantidadS"]*datos_g["densidad"]), #
            "vinilo" : (colino)*preparacion["vinilo"]["cantidadS"]*preparacion["vinilo"]["frecuencia"]/1000,#
            "paecilomyces" :(colino*preparacion["paecilomyces"]["cantidadS"]*preparacion["paecilomyces"]["frecuencia"]),
            "trichoderma" :(colino*preparacion["trichoderma"]["cantidadS"]*preparacion["trichoderma"]["frecuencia"]),
            "melaza" :(colino)*preparacion["melaza"]["cantidadS"]*preparacion["melaza"]["frecuencia"]/1000,
        }

        ci_costo ={
            "materiaOrganica" : [],
            "herbicidaCalles" : [],
            "herbicidaPlatos" : [],
            "insecticidas" : [],
            "fungicidas" : [],
            "fertilizante" : [],
            "ridomil" : [],
            "fertilizanteFoliar" : [],
            "biocontroladores" : [],
            "guadana" : [],
            "selectores" : [],
            "bombasEspalda" : [],
            "bombasEstacionarias" : [],
            "canastillas" : [],
            "herramientas" : [],
            "lycra" : []
        }
        for key,value in costos_insumos.iteritems():
            if key == "herbicidaCalles":
                    for counter,d in enumerate(value):
                        if counter < 2:
                            ci_costo[key].append(datos_g["densidad"]*d["cantidadS"]*d["frecuencia"]/2/1000)
                        else:
                            ci_costo[key].append(datos_g["densidad"]*d["cantidadS"]*d["frecuencia"]/1000)
            else:
                for d in value:
                    ci_costo[key].append(datos_g["densidad"]*d["cantidadS"]*d["frecuencia"])

        subTotalInsumos = {
            "colino":[self.insumos_g.arbol*pmo_costo["colino"]/1000],
            "estacas":[ pmo_costo["estacas"]/1000 ],
            "cal":[ pmo_costo["cal"]/1000 ],
            "dap":[ pmo_costo["dap"]/1000 ],
            "micorriza":[pmo_costo["micorriza"]/1000],
            "vinilo":[ pmo_costo["vinilo"]/1000 ],
            "paecilomyces":[ pmo_costo["paecilomyces"]/1000 ],
            "trichoderma":[ pmo_costo["trichoderma"]/1000 ],
            "melaza":[ pmo_costo["melaza"]/1000 ],
            "materiaOrganica":[],
            "herbicidaCalles":[],
            "herbicidaPlatos":[],
            "insecticidas":[],
            "fungicidas":[],
            "fertilizante":[],
            "ridomil":[],
            "fertilizanteFoliar":[],
            "biocontroladores":[],
            "guadana":[],
            "selectores":[],
            "bombasEspalda":[],
            "bombasEstacionarias":[],
            "canastillas":[],
            "herramientas":[],
            "lycra":[]
        }

        cost = {"materiaOrganica":self.insumos_g.materiaOrganica, "herbicidaCalles":self.insumos_g.herbicida, "herbicidaPlatos":self.insumos_g.herbicida,
        "insecticidas":self.insumos_g.insecticida, "fungicidas": self.insumos_g.fungicida, "fertilizante":self.insumos_g.fertilizante, 
        "ridomil": self.insumos_g.ridomil, "fertilizanteFoliar": self.insumos_g.fertilizante}

        for key,value in cost.iteritems():
            for f in ci_costo[key]:
                subTotalInsumos[key].append(value*f/1000)

        ############
        keys = ["biocontroladores", "guadana", "selectores", "bombasEspalda", "bombasEstacionarias", "canastillas", "herramientas", "lycra"]
        for k in keys:
            for f in ci_costo[k]:
                subTotalInsumos[k].append(f/1000)
        ############
        totalInsumos = [0,0,0,0,0,
                        0,0,0,0,0,
                        0,0,0,0,0]

        for key,value in subTotalInsumos.iteritems():
            for counter,x in enumerate(value):
                totalInsumos[counter] = totalInsumos[counter] + x

        return totalInsumos
        

    def IngresosEgresos(self):
    # Datos
        dc_produccion = self.distribucion_calidad.getValues()
        datos_g = self.datos_g.getValues()
        insumos_g = self.insumos_g.getValues()
        establecimiento = self.establecimiento_r.getValues()
        insumos_mo = self.insumos_mo.getValues()
    # INGRESOS
    # Ventas (ingreses)
        ventas = []
        for tkg in dc_produccion["produccion"]:
            ventas.append(
                    tkg*(dc_produccion["primera"]["mult"] + dc_produccion["tercera"]["mult"] + dc_produccion["segunda"]["mult"])
                )

    # EGRESOS (perdidas)
        egresos = []

    # COSTOS INDIRECTOS PRODUCCION Y COMERCIALIZACIÓN
        cipc = self.cipc.getSums()

    # MANO DE OBRA
        leldpE = establecimiento
    # Labores de Establecimiento, Levante, Desarrollo y Producción.
        leldpE["preparacionTerreno"] = establecimiento["preparacionTerreno"]
        leldpE["trazo"] = establecimiento["trazo"]*datos_g["densidad"]
        leldpE["hoyado"] = establecimiento["hoyado"]*datos_g["densidad"]
        leldpE["distribucionColino"] = establecimiento["distribucionColino"]*datos_g["densidad"]
        leldpE["aplicacionCorrectivos"] = establecimiento["aplicacionCorrectivos"]*datos_g["densidad"]
        leldpE["aplicacionMicorriza"] = establecimiento["aplicacionMicorriza"]*datos_g["densidad"]
        leldpE["aplicacionMateriaOrganica"] = establecimiento["aplicacionMateriaOrganica"]*datos_g["densidad"]
        leldpE["siembra"] = establecimiento["siembra"]*datos_g["densidad"]
        leldpE["resiembra"] = establecimiento["resiembra"]*datos_g["densidad"]

        leldpR = {
            "siembra" : [],
            "resiembra" : [],
            "limpiaGuadanaCalles" : [],
            "aplicacionHerbicida" : [],
            "plateo" : [],
            "fertilizacion" : [],
            "aplicacionMateriaOrganica" : [],
            "fungicidas" : [],
            "biocontroladores" : [],
            "aspersiones" : [],
            "tutorado" : [],
            "podas" : []
        }

        recoleccion = {
            "recoleccionContrato": [],
            "recoleccionDia": []
        }

        for data_mo in insumos_mo["siembra"]:
            leldpR["siembra"].append(data_mo["rendimiento"]*data_mo["frecuencia"])

        for data_mo in insumos_mo["resiembra"]:
            leldpR["resiembra"].append(data_mo["rendimiento"]*data_mo["frecuencia"])

        for data_mo in insumos_mo["limpiaGuadanaCalles"]:
            leldpR["limpiaGuadanaCalles"].append(data_mo["rendimiento"]*data_mo["frecuencia"])

        for data_mo in insumos_mo["aplicacionHerbicida"]:
            leldpR["aplicacionHerbicida"].append(data_mo["rendimiento"]*data_mo["frecuencia"])

        keys = [ "plateo", "fertilizacion", "aplicacionMateriaOrganica", "fungicidas", "biocontroladores", "aspersiones", "tutorado", "podas"]
        for k in keys:
            for data_mo in insumos_mo[k]:
                if data_mo["rendimiento"]*data_mo["frecuencia"] == 0:
                    leldpR[k].append(0)
                else:
                    leldpR[k].append(datos_g["densidad"]/data_mo["rendimiento"]*data_mo["frecuencia"])


        for counter,data_mo in enumerate(insumos_mo["recoleccionContrato"]):
            div = data_mo["rendimiento"]*data_mo["frecuencia"]
            if div == 0:
                recoleccion["recoleccionContrato"].append(0)
            else:
                recoleccion["recoleccionContrato"].append(
                    (
                        70*dc_produccion["produccion"][counter]/100)/div
                    )

        for counter,data_mo in enumerate(insumos_mo["recoleccionDia"]):
            div = data_mo["rendimiento"]*data_mo["frecuencia"]
            if div == 0:
                recoleccion["recoleccionDia"].append(0)
            else:
                recoleccion["recoleccionDia"].append(
                    (
                        30*dc_produccion["produccion"][counter]/100)/data_mo["rendimiento"]*data_mo["frecuencia"]
                    )

        subTotalMO = [0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0]

        for key, value in leldpE.iteritems():
            subTotalMO[0] = subTotalMO[0] + value

        for k, v in leldpR.iteritems():
            for counter,i in enumerate(subTotalMO):
                subTotalMO[counter] = subTotalMO[counter] + v[counter]

    # Recolección
        subTotalRecoleccion = [0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0]

        for k, v in recoleccion.iteritems():
            for counter,i in enumerate(subTotalRecoleccion):
                subTotalRecoleccion[counter] = subTotalRecoleccion[counter] + v[counter]

        totalRecoleccion = []
        totalLEL = []
        totalMO = []

        for i in subTotalMO:
            totalLEL.append(i*datos_g["jornal"]/1000)

        for i in subTotalRecoleccion:
            totalRecoleccion.append( i*datos_g["jornal"]/1000)

        for i in range(len(totalRecoleccion)):
            totalMO.append(totalLEL[i] + totalRecoleccion[i])

    # INSUMOS
        totalInsumos = self.totalInsumos()

    # result
        for x in range(0,15):
            egresos.append((totalMO[x] + cipc[x] + totalInsumos[x])*-10) #Agregado según excel es por -1000 pero en la gráfica es demasiado entonces -10

        return {"ingresos":ventas, "egresos": egresos}

    def margen(self):
        ie = self.IngresosEgresos()
        egresos = ie["egresos"]
        ingresos = ie["ingresos"]
        margen = []
        for i in range(len(ingresos)):
            margen.append(ingresos[i]+egresos[i])

        return margen
            
        
class lote_has_bp(models.Model):
    lote = models.ForeignKey(Lote, blank=False, related_name= "lotebp_lote")
    bp = models.ForeignKey(Base_presupuestal, blank=False, related_name= "lotebp_bp")