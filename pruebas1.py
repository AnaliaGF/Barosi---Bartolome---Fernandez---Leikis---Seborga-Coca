
#Enlaces útiles
    # Enlace CRUD peewee:
    # https://docs.peewee-orm.com/en/latest/peewee/querying.html

import io
import datetime

from peewee import *

# ESTO VIENE DEL IMPORT IO

datoscabaarchivo = open("E:\observatorio-de-obras-urbanas.csv", "r", encoding="utf-8")

# ESTO VIENE DEL IMPORT IO


# ESTO VIENE DE PEEWEE

datoscabadb = SqliteDatabase("E:\obrascaba.db")

class BaseModel(Model):
    id = PrimaryKeyField()
    nombre = CharField()
    class Meta:
        database = datoscabadb

class Entorno(BaseModel):
    pass

class Etapa(BaseModel):
    pass

class Obra(BaseModel):
    descripcion = CharField()
    monto_contrato = IntegerField(null=True)
    entorno_id = IntegerField()
    etapa_id = IntegerField()

# CREA LAS TABLAS EN LA DB
datoscabadb.create_tables([Entorno, Etapa, Obra])

# ESTO VIENE DE PEEWEE

datoscabaarchivo.readline()

for linea in datoscabaarchivo:
    
    lista = linea.split(",")

    # DEFINICION CAMPOS­

    obra_nombre = lista[2].upper().strip().replace('"', '').replace('­', '')
    obra_descripcion = lista[6].upper().strip().replace('"', '').replace('­', '')
    obra_monto_contrato = lista[7].upper().strip().replace('"', '').replace('­', '')
    entorno_nombre = lista[1].upper().strip().replace('"', '').replace('­', '')
    etapa_nombre = lista[3].upper().strip().replace('"', '').replace('­', '')
    
    # DEFINICION CAMPOS

    # ENTORNO

    entorno_id = None

    if entorno_nombre !=  '':

        entorno_id = Entorno.select(Entorno.id).where(Entorno.nombre == entorno_nombre).first()
        
        if entorno_id == None:
            entorno = Entorno(nombre = entorno_nombre)
            entorno.save()
            entorno_id = entorno.id  

    # ENTORNO

    # ETAPA

    etapa_id = None

    if etapa_nombre !=  '':

        etapa_id = Etapa.select(Etapa.id).where(Etapa.nombre == etapa_nombre).first()
        
        if etapa_id == None:
            etapa = Etapa(nombre = etapa_nombre)
            etapa.save()
            etapa_id = etapa.id       

    # ETAPA

    # OBRA
    
    if obra_nombre != '' and entorno_id != '' and etapa_id != '':

        obra = Obra()
        obra.nombre = obra_nombre
        obra.descripcion = obra_descripcion
        obra.monto_contrato = obra_monto_contrato
        obra.entorno_id = entorno_id
        obra.etapa_id = etapa_id
        obra.save()

    # OBRA

 # esto es de clave foranea
    class Role(BaseModel):
        """ Field Types """
        role_id = PrimaryKeyField()
        rolename = CharField(25)

    class Meta:
        db_table = 'roles'

class User(BaseModel):
    """ Field Types """
    user_id = PrimaryKeyField()
    username = CharField(25)
    role = ForeignKeyField(Role, to_field="role_id")

  