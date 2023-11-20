from abc import ABC
from modelo_orm import *
from peewee import fn
import pandas as pd
import numpy as np
import math

class GestionarObra(ABC):    
    df = pd.DataFrame()
    data = []

    @classmethod
    def extraer_datos(cls):
        cls.df = pd.read_csv("observatorio-de-obras-urbanas.csv")
        #.replace("", " ", regex=True)

    @classmethod
    def conectar_db(cls):
        db.initialize(SqliteDatabase("obras_urbanas.db"))

    @classmethod
    def mapear_orm(cls):
        db.create_tables([Entorno, Etapa, Tipo_obra, Contratacion_tipo, Area_responsable, Barrio, Empresa, Obra])

    @classmethod
    def limpiar_datos(cls):
        # Eliminar filas con valores nulos en columnas importantes
        cols_a_considerar = [
            "nombre",
            "monto_contrato",
            "fecha_inicio",
            "fecha_fin_inicial",
            "porcentaje_avance",
        ]
        cls.df = cls.df.dropna(subset=cols_a_considerar)

        # Manejar valores nulos en otras columnas
        cls.df["descripcion"].fillna("Sin descripcion", inplace=True)
        cls.df["area_responsable"].fillna("Sin area responsable", inplace=True)      

        # Elimina el caracter extraño que se encuentra en algunas palabras acentuadas, reemplaza simbolo por ñ. 
        # Elimina acentos, convierte todo a mayuscula y elimina espacios iniciales y finales de modo de minimizar las repeticiones
        cls.df = cls.df.replace('­', '', regex=True).replace('Ã±', 'ñ', regex=True).replace('á','a', regex=True).replace('é','e', regex=True).replace('í','i', regex=True).replace('ó','o', regex=True).replace('ú', 'u', regex=True).astype(str).apply(lambda col: col.str.upper().str.strip())

        for index, row in cls.df.iterrows():
          
            # Reemplaza los caracteres que separan multiples barrios (",", "/", "A" e "Y") por el caracter "|"
            barriopaso1 = cls.df["barrio"][index].replace(',', '|').replace('/', '|').replace(' A ', '|').replace(' Y ', '|')

            # Crea una lista dividiendo los datos usando el caracter "|" como criterio de division. 
            barriopaso2  = barriopaso1.split('|')
            
            # De la lista creada en barriopaso2 elije el primero elemento (indice 0).
            # Elimina los espacios adelante y atras.
            barriopaso3 = barriopaso2[0].strip()

            # Reemplaza el valor original del DataFrame con el obtenido en barriopaso3
            cls.df["barrio"][index] = barriopaso3
            
            # Hace lo mismo que en barrio, pero para comuna en una sola linea
            cls.df["comuna"][index] = row["comuna"].replace(',', '|').replace('/', '|').replace(' A ', '|').replace(' Y ', '|').split('|')[0].strip()

            # Elimina el simbolo '%' y cambia los '.' por ',' que es el separado de decimales definido.
            cls.df["porcentaje_avance"][index] = cls.df["porcentaje_avance"][index].replace('%', '').replace(',', '.').strip()
           
            try:
                aux_plazo = math.ceil(float(cls.df["plazo_meses"][index].replace(',', '.').strip()))
            except ValueError:
                aux_plazo = None         

            cls.df["plazo_meses"][index] = aux_plazo

    @classmethod
    def cargar_datos(cls):
        
        # Ejecuta los queries envueltos en una transaccion
        with db.atomic() as transaction:     

            try:

                # Itera sobre las filas del DataFrame y crea instancias de las clases del modelo ORM
                for index, row in cls.df.iterrows():
                    # Crea instancias de las clases del modelo ORM con los datos de cada fila
                    entorno = Entorno.get_or_create(nombre=row["entorno"])
                    etapa = Etapa.get_or_create(nombre=row["etapa"])                
                    tipo_obra = Tipo_obra.get_or_create(nombre=row["tipo"])
                    area_responsable = Area_responsable.get_or_create(nombre=row["area_responsable"])
                    barrio = Barrio.get_or_create(nombre=row["barrio"], comuna=row["comuna"])
                    empresa = Empresa.get_or_create(nombre=row["licitacion_oferta_empresa"], cuit=row["cuit_contratista"])
                    contratacion_tipo = Contratacion_tipo.get_or_create(nombre=row["contratacion_tipo"])

                    obra = Obra.create(
                        nombre=row["nombre"],
                        id_entorno=entorno[0],
                        id_etapa=etapa[0],
                        id_tipo_obra=tipo_obra[0],
                        id_contratacion_tipo=contratacion_tipo[0],
                        id_area_responsable=area_responsable[0],
                        descripcion=row["descripcion"],
                        monto_contrato=row["monto_contrato"],
                        id_barrio=barrio[0],
                        direccion=row["direccion"],
                        fecha_inicio=row["fecha_inicio"],
                        fecha_fin_inicial=row["fecha_fin_inicial"],
                        plazo_meses=row["plazo_meses"],
                        porcentaje_avance=row["porcentaje_avance"],
                        imagen_1=row["imagen_1"],
                        imagen_2=row["imagen_2"],
                        imagen_3=row["imagen_3"],
                        imagen_4=row["imagen_4"],
                        id_empresa=empresa[0],
                        licitacion_anio=row["licitacion_anio"],
                        nro_contratacion=row["nro_contratacion"],
                        mano_obra=row["mano_obra"],
                        numero_expediente=row["expediente-numero"],
                        destacada=row["destacada"],
                        fuente_financiamiento=row["financiamiento"],
                    )

                    # Agregar mensaje de impresión
                    print(f"Obra cargada: {obra.nombre}")
                    # Persiste la nueva instancia de Obra en la base de datos
                    obra.save()
                    print("Datos cargados correctamente en la base de datos.")
                
                transaction.commit()
            
            except DatabaseError:
            
                transaction.rollback()

    @classmethod
    def nueva_obra(cls):
        
        # Opcion 1
        # return Obra()


        # Opcion 2

        nombre = input("Ingrese el nombre: ")
        descripcion = input("Ingrese la descripcion: ")

        while True:
            try:
                tipo_obra = Tipo_obra.get(nombre=input("Ingrese el tipo de obra: "))
            except:
                print("Tipo de Obra inexistente.")
                continue
            else:
                break
 
        while True:
            try:
                area_responsable = Area_responsable.get(nombre=input("Ingrese el área responsable: "))
            except:
                print("Área responsable inexistente.")
                continue
            else:
                break

        while True:
            try:
                barrio = Barrio.get(nombre=input("Ingrese el nombre del barrio: "))
            except:
                print("Nombre de barrio inexistente.")
                continue
            else:
                break
        
        obra = Obra()
        obra.nombre = nombre
        obra.descripcion = descripcion
        obra.id_tipo_obra = tipo_obra
        obra.id_area_responsable = area_responsable
        obra.id_barrio = barrio

        if (obra.nuevo_proyecto() == True):
            print("Nuevo proyecto de obra creado.")
            return obra 
        else:
            print("No se pudo crear la nueva obra porque faltaron datos obligatorios.")
            return None

    #@classmethod
    #def obtener_indicadores(cls):

    #Indicadores que faltan:
        # a.Listado de todas las áreas responsables
        # b.Listado de todos los tipos de obra.

        # c.Cantidad de obras que se encuentran en cada etapa:
        #  obras_por_etapa = (
        #                     Etapa
        #                         .select(Etapa.nombre.alias('etapa'), fn.COUNT(Obra.id).alias('cantidad'))
        #                         .join(Obra, JOIN.LEFT_OUTER)
        #                         .group_by(Etapa.nombre)
        #                   ).execute()

        # print(obras_por_etapa)

        # for fila in obras_por_etapa:
        #     print(fila.etapa, fila.cantidad)
        
    #Más indicadores que faltan
        # d.Cantidad de obras y monto total de inversión por tipo de obra.
        # e.Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3.
        # f.Cantidad de obras finalizadas y su y monto total de inversión en la comuna 1.
        # g.Cantidad de obras finalizadas en un plazo menor o igual a 24 meses
        # h.Porcentaje total de obras finalizadas.
        # i.Cantidad total de mano de obra empleada.
        # j.Monto total de inversión.


            # # Contar el número total de obras
            # total_obras = Obra.select().count()

            # if total_obras == 0:
            #     print("No hay obras en la base de datos.")
            #     return

            # # Agrega estas líneas para imprimir información adicional
            # obras_con_avance = Obra.select().where(Obra.porcentaje_avance.is_null(False))

            # # Calcular el monto total de los contratos
            # monto_total_contratos = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()

            # # Calcular el porcentaje promedio de avance
            # porcentaje_promedio_avance = Obra.select(fn.AVG(Obra.porcentaje_avance)).scalar()

            # # Obtener la obra con el mayor porcentaje de avance
            # obra_mayor_avance = (Obra.select().order_by(Obra.porcentaje_avance.desc()).first())

            # print(f"Obras con porcentaje de avance: {obras_con_avance.count()}")                
            # print(f"Número total de obras: {total_obras}")
            # print(f"Monto total de contratos: {monto_total_contratos}")
            # print(f"Porcentaje promedio de avance: {porcentaje_promedio_avance}")
            # print(f"Obra con mayor porcentaje de avance: {obra_mayor_avance.descripcion}")

    def chequear_base(cls):
        if len(db.get_tables()) > 0:
            return True
        else:
            return False
