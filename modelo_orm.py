import datetime
from peewee import *

#db = SqliteDatabase("obras_urbanas.db")
db = Proxy()

class BaseModel(Model):
    id = PrimaryKeyField()
    nombre = CharField()
    class Meta:
        database = db

class etapa(BaseModel):
    pass

class tipo_obra(BaseModel):
    pass

class tipo_licitacion(BaseModel):
    pass

class area_responsable(BaseModel):
    pass

class barrio(BaseModel):
    comuna = CharField()
    
class empresa(BaseModel):
    cuit = CharField()

class obra(BaseModel):
    entorno = CharField()
    id_etapa = ForeignKeyField(etapa, to_field="id")
    id_tipo_obra = ForeignKeyField(tipo_obra, to_field="id", null=True)
    id_area_responsable = ForeignKeyField(area_responsable, to_field="id", null=True)
    descripcion = CharField(null=True)
    monto_contrato = IntegerField(null=True)
    id_barrio = ForeignKeyField(barrio, to_field="id")
    direccion = CharField(null=True)
    latitud =  CharField(null=True)
    longitud =  CharField(null=True)
    fecha_inicio = DateTimeField(null=True)
    fecha_fin_inicial =  DateTimeField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje_avance = FloatField(null=True) 
    imagen_1 = CharField(null=True)
    imagen_2 = CharField(null=True)
    imagen_3 = CharField(null=True)
    imagen_4 = CharField(null=True)
    id_empresa =  ForeignKeyField(empresa, to_field="id", null=True)
    licitacion_anio = IntegerField(null=True)
    id_licitacion =  ForeignKeyField(tipo_licitacion, to_field="id", null=True)
    nro_contratacion = CharField(null=True)
    beneficiario = CharField(null=True)
    link_interno = CharField(null=True)
    pliego_descarga = CharField(null=True)
    expediente_numero = CharField(null=True)
