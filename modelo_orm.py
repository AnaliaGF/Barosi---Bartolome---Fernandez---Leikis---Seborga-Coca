import datetime
from peewee import *

# db = SqliteDatabase("obras_urbanas.db")
db = Proxy()

class BaseModel(Model):
    id = PrimaryKeyField()
    nombre = CharField()

    class Meta:
        database = db

class Etapa(BaseModel):
    pass

class Tipo_obra(BaseModel):
    pass

class Area_responsable(BaseModel):
    pass

class Barrio(BaseModel):
    comuna = CharField()

class Empresa(BaseModel):
    cuit = CharField()

class Tipo_licitacion(BaseModel):
    pass

class Obra(BaseModel):
    entorno = CharField()
    id_etapa = ForeignKeyField(Etapa, to_field="id")
    id_tipo_obra = ForeignKeyField(Tipo_obra, to_field="id", null=True)
    id_area_responsable = ForeignKeyField(Area_responsable, to_field="id", null=True)
    descripcion = CharField(null=True)
    monto_contrato = IntegerField(null=True)
    id_barrio = ForeignKeyField(Barrio, to_field="id")
    direccion = CharField(null=True)
    fecha_inicio = DateTimeField(null=True)
    fecha_fin_inicial = DateTimeField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje_avance = FloatField(null=True)
    imagen_1 = CharField(null=True)
    imagen_2 = CharField(null=True)
    imagen_3 = CharField(null=True)
    imagen_4 = CharField(null=True)
    id_empresa = ForeignKeyField(Empresa, to_field="id", null=True)
    licitacion_anio = IntegerField(null=True)
    id_licitacion = ForeignKeyField(Tipo_licitacion, to_field="id", null=True)
    nro_contratacion = CharField(null=True)