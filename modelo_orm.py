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
    pass


class Empresa(BaseModel):
    cuit = CharField()


class Tipo_licitacion(BaseModel):
    pass

class Obra(BaseModel):
    entorno = CharField()
    id_etapa = ForeignKeyField(Etapa, to_field="id", db_column="id_etapa")
    id_tipo_obra = ForeignKeyField(
        Tipo_obra, to_field="id", null=True, db_column="id_tipo_obra"
    )
    id_area_responsable = ForeignKeyField(
        Area_responsable, to_field="id", null=True, db_column="id_area_responsable"
    )
    descripcion = CharField(null=True)
    monto_contrato = IntegerField(null=True)
    id_barrio = ForeignKeyField(Barrio, to_field="id", db_column="id_barrio")
    direccion = CharField(null=True)
    fecha_inicio = DateTimeField(null=True)
    fecha_fin_inicial = DateTimeField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje_avance = FloatField(null=True)
    imagen_1 = CharField(null=True)
    imagen_2 = CharField(null=True)
    imagen_3 = CharField(null=True)
    imagen_4 = CharField(null=True)
    id_empresa = ForeignKeyField(
        Empresa, to_field="id", null=True, db_column="id_empresa"
    )
    licitacion_anio = IntegerField(null=True)
    id_licitacion = ForeignKeyField(
        Tipo_licitacion, to_field="id", null=True, db_column="id_licitacion"
    )
    nro_contratacion = CharField(null=True)
    mano_obra = CharField(null=True)

# Inicio Ejercicio 5

    def nuevo_proyecto(self):
        if self.id_etapa is not None:
            nueva_etapa_id = 13
        else:
            try:
                nueva_etapa = Etapa.get(Etapa.nombre == "Proyecto")
                nueva_etapa_id = nueva_etapa.id
            except DoesNotExist:
                nueva_etapa = Etapa.create(nombre="Proyecto")
                nueva_etapa_id = nueva_etapa.id
    
        self.id_etapa = nueva_etapa_id
        self.save()
    
        print("Nuevo proyecto de obra iniciado.")
    
        def iniciar_contratacion(self):
            pass
          
        def adjudicar_obra(self):
            pass
          
        def iniciar_obra(self):
            pass
          
        def actualizar_porcentaje_avance(self):
            pass
          
        def incrementar_plazo(self):
            pass
          
        def incrementar_mano_obra(self):
            pass
          
        def finalizar_obra(self):
            pass        