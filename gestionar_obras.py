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

    classmethod
    def nueva_obra(cls):
       
       def limpiar_input(input_text):
           # Convierte a mayúsculas, elimina espacios al inicio y al final, y quita tildes
           return input_text.upper().strip().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    
       # Opción 1
       # return Obra()
    
       # Opción 2
       nombre = limpiar_input(input("Ingrese el nombre: "))
       descripcion = limpiar_input(input("Ingrese la descripción: "))
       
       while True:
           try:
               tipo_obra = Tipo_obra.get(nombre=limpiar_input(input("Ingrese el tipo de obra: ")))
           except:
               print("Tipo de Obra inexistente.")
               continue
           else:
               break
            
       while True:
           try:
               area_responsable = Area_responsable.get(nombre=limpiar_input(input("Ingrese el área responsable: ")))
           except:
               print("Área responsable inexistente.")
               continue
           else:
               break
            
       while True:
           try:
               barrio = Barrio.get(nombre=limpiar_input(input("Ingrese el nombre del barrio: ")))
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
    
       if obra.nuevo_proyecto():
           print("Nuevo proyecto de obra creado.")
           return obra
       else:
           print("No se pudo crear la nueva obra porque faltaron datos obligatorios.")
           return None

    @classmethod
    def obtener_indicadores(cls):

    #     a.Listado de todas las áreas responsables:
        areas_responsables = [area.nombre for area in Area_responsable.select()]
        print("Listado de todas las áreas responsables:", areas_responsables)

    #     b.Listado de todos los tipos de obra:
        tipos_obras = [tipo_obra.nombre for tipo_obra in Tipo_obra.select()]
        print("Listado de todos los tipos de obra:", tipos_obras)

    #     c.Cantidad de obras que se encuentran en cada etapa:
        obras_por_etapa = (
                            Etapa
                                .select(Etapa.nombre.alias('etapa'), fn.COUNT(Obra.id).alias('cantidad'))
                                .join(Obra, JOIN.LEFT_OUTER)
                                .group_by(Etapa.nombre)
                          ).execute()

        for fila in obras_por_etapa:
            print(f"Cantidad de obras en la etapa {fila.etapa}: {fila.cantidad}")
        
    #     d.Cantidad de obras y monto total de inversión por tipo de obra:

        obras_por_tipo = (
            Tipo_obra
            .select(Tipo_obra.nombre, fn.COUNT(Obra.id).alias('cantidad'), fn.SUM(Obra.monto_contrato).alias('monto_total'))
            .join(Obra)
            .group_by(Tipo_obra)
        )
        for tipo_obra in obras_por_tipo:
            print(f"Cantidad de obras de tipo {tipo_obra.nombre}: {tipo_obra.cantidad}, Monto total de inversión: ${round(tipo_obra.monto_total, 2)}")

    #     e.Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3.

        comunas = [1, 2, 3]
        barrios_comunas = (
            Barrio
            .select()
            .join(Obra)
            .where(Obra.id_barrio.in_(comunas))
            .distinct()
        )
        for barrio in barrios_comunas:
            print(f"Barrio perteneciente a comunas 1, 2 o 3: {barrio.nombre}")

    #     f.Cantidad de obras finalizadas y su y monto total de inversión en la comuna 1:

        obras_finalizadas_comuna1 = (
            Obra
            .select(fn.COUNT(Obra.id).alias('cantidad'), fn.SUM(Obra.monto_contrato).alias('monto_total'))
            .where((Obra.id_etapa == 1) & (Obra.id_barrio == 1))
        ).first()

        print(f"Cantidad de obras finalizadas en la comuna 1: {obras_finalizadas_comuna1.cantidad}")
        print(f"Monto total de inversión en la comuna 1: ${round(obras_finalizadas_comuna1.monto_total, 2)}")

    #     g.Cantidad de obras finalizadas en un plazo menor o igual a 24 meses:

        obras_finalizadas_24_meses = (
            Obra
            .select(fn.COUNT(Obra.id).alias('cantidad'))
            .where((Obra.id_etapa == 1) & (Obra.plazo_meses <= 24))
        ).scalar()

        print(f"Cantidad de obras finalizadas en un plazo menor o igual a 24 meses: {obras_finalizadas_24_meses}")

    #     h.Porcentaje total de obras finalizadas:

        total_obras_finalizadas = Obra.select(fn.COUNT(Obra.id)).where(Obra.id_etapa == 1).scalar()
        total_obras = Obra.select(fn.COUNT(Obra.id)).scalar()
        porcentaje_obras_finalizadas = (total_obras_finalizadas / total_obras) * 100
        
        print(f"Porcentaje total de obras finalizadas: {round(porcentaje_obras_finalizadas, 2)}%")

    #     i.Cantidad total de mano de obra empleada:

        mano_obra_total = Obra.select(fn.SUM(Obra.mano_obra)).scalar()

        print(f"Cantidad total de mano de obra empleada: {mano_obra_total}")

    #     j.Monto total de inversión:

        monto_total_inversion = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()

        print(f"Monto total de inversión: ${round(monto_total_inversion, 2)}")

    def chequear_base(cls):
        if len(db.get_tables()) > 0:
            return True
        else:
            return False