from abc import ABC
from modelo_orm import *
from peewee import fn
import pandas as pd


class GestionarObra(ABC):
    df = pd.DataFrame()
    data = []

    @classmethod
    def extraer_datos(cls):
        cls.df = pd.read_csv("observatorio-de-obras-urbanas.csv").replace(
            "", " ", regex=True
        )

    @classmethod
    def conectar_db(cls):
        db.initialize(SqliteDatabase("obras_urbanas.db"))

    @classmethod
    def mapear_orm(cls):
        db.create_tables(
            [Etapa, Tipo_obra, Tipo_licitacion, Area_responsable, Barrio, Empresa, Obra]
        )

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
        cls.df["descripcion"].fillna("Sin descripción", inplace=True)
        cls.df["area_responsable"].fillna("Sin área responsable", inplace=True)

        # Eliminar espacios en blanco adicionales en columnas de tipo cadena
        cls.df["nombre"] = cls.df["nombre"].str.strip()
        cls.df["descripcion"] = cls.df["descripcion"].str.strip()

    @classmethod
    def cargar_datos(cls):
        # Itera sobre las filas del DataFrame y crea instancias de las clases del modelo ORM
        for index, row in cls.df.iterrows():
            # Crea instancias de las clases del modelo ORM con los datos de cada fila
            etapa = Etapa.create(nombre=row["etapa"])
            tipo_obra = Tipo_obra.create(nombre=row["tipo"])
            area_responsable = Area_responsable.create(nombre=row["area_responsable"])
            barrio = Barrio.create(nombre=row["barrio"], comuna=row["comuna"])
            empresa = Empresa.create(
                nombre=row["licitacion_oferta_empresa"], cuit=row["cuit_contratista"]
            )
            tipo_licitacion = Tipo_licitacion.create(nombre=row["contratacion_tipo"])

            obra = Obra.create(
                nombre=row["nombre"],
                entorno=row["entorno"],
                id_etapa=etapa,
                id_tipo_obra=tipo_obra,
                id_tipo_licitacion=tipo_licitacion,
                id_area_responsable=area_responsable,
                descripcion=row["descripcion"],
                monto_contrato=row["monto_contrato"],
                id_barrio=barrio,
                direccion=row["direccion"],
                fecha_inicio=row["fecha_inicio"],
                fecha_fin_inicial=row["fecha_fin_inicial"],
                plazo_meses=row["plazo_meses"],
                porcentaje_avance=row["porcentaje_avance"],
                imagen_1=row["imagen_1"],
                imagen_2=row["imagen_2"],
                imagen_3=row["imagen_3"],
                imagen_4=row["imagen_4"],
                id_empresa=empresa,
                licitacion_anio=row["licitacion_anio"],
                nro_contratacion=row["nro_contratacion"],
            )

            # Agregar mensaje de impresión
            print(f"Obra cargada: {obra.nombre}")
            # Persiste la nueva instancia de Obra en la base de datos
            obra.save()
            print("Datos cargados correctamente en la base de datos.")

    @classmethod
    def nueva_obra(cls):
          nombre = input("Ingrese el nombre: ")
          entorno = input("Ingrese el entorno: ")
          etapa_nombre = input("Ingrese la etapa: ")
          tipo_obra_nombre = input("Ingrese el tipo de obra: ")
          tipo_licitacion_nombre = input("Ingrese el tipo de licitación: ")
          area_responsable_nombre = input("Ingrese el área responsable: ")
          descripcion = input("Ingrese la descripción: ")
          monto_contrato = int(input("Ingrese el monto del contrato: "))
          barrio_nombre = input("Ingrese el nombre del barrio: ")
          comuna = input("Ingrese la comuna: ")
          direccion = input("Ingrese la dirección: ")
          fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
          fecha_fin_inicial = input("Ingrese la fecha de fin inicial (YYYY-MM-DD): ")
          plazo_meses = int(input("Ingrese el plazo en meses: "))
          porcentaje_avance = float(input("Ingrese el porcentaje de avance: "))
          imagen_1 = input("Ingrese la URL de la imagen 1: ")
          imagen_2 = input("Ingrese la URL de la imagen 2: ")
          imagen_3 = input("Ingrese la URL de la imagen 3: ")
          imagen_4 = input("Ingrese la URL de la imagen 4: ")
          empresa_nombre = input("Ingrese el nombre de la empresa: ")
          empresa_cuit = input("Ingrese el CUIT de la empresa: ")
          licitacion_anio = int(input("Ingrese el año de la licitación: "))
          nro_contratacion = input("Ingrese el número de contratación: ")

          etapa, _ = Etapa.get_or_create(nombre=etapa_nombre)
          tipo_obra, _ = Tipo_obra.get_or_create(nombre=tipo_obra_nombre)
          tipo_licitacion, _ = Tipo_licitacion.get_or_create(nombre=tipo_licitacion_nombre)
          area_responsable, _ = Area_responsable.get_or_create(nombre=area_responsable_nombre)
          barrio, _ = Barrio.get_or_create(nombre=barrio_nombre, comuna=comuna)
          empresa, _ = Empresa.get_or_create(nombre=empresa_nombre, cuit=empresa_cuit)

          obra = Obra.create(
              nombre=nombre,
              entorno=entorno,
              id_etapa=etapa,
              id_tipo_obra=tipo_obra,
              id_tipo_licitacion=tipo_licitacion,
              id_area_responsable=area_responsable,
              descripcion=descripcion,
              monto_contrato=monto_contrato,
              id_barrio=barrio,
              direccion=direccion,
              fecha_inicio=fecha_inicio,
              fecha_fin_inicial=fecha_fin_inicial,
              plazo_meses=plazo_meses,
              porcentaje_avance=porcentaje_avance,
              imagen_1=imagen_1,
              imagen_2=imagen_2,
              imagen_3=imagen_3,
              imagen_4=imagen_4,
              id_empresa=empresa,
              licitacion_anio=licitacion_anio,
              nro_contratacion=nro_contratacion,
          )

          print("Nueva obra creada y persistida correctamente.")

          return obra

    @classmethod
    def obtener_indicadores(cls):
        # Contar el número total de obras
        total_obras = Obra.select().count()

        if total_obras == 0:
            print("No hay obras en la base de datos.")
            return

        # Agrega estas líneas para imprimir información adicional
        obras_con_avance = Obra.select().where(Obra.porcentaje_avance.is_null(False))
        print(f"Obras con porcentaje de avance: {obras_con_avance.count()}")

        # Calcular el monto total de los contratos
        monto_total_contratos = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()

        # Calcular el porcentaje promedio de avance
        porcentaje_promedio_avance = Obra.select(
            fn.AVG(Obra.porcentaje_avance)
        ).scalar()

        # Obtener la obra con el mayor porcentaje de avance
        obra_mayor_avance = (
            Obra.select().order_by(Obra.porcentaje_avance.desc()).first()
        )

        print(f"Número total de obras: {total_obras}")
        print(f"Monto total de contratos: {monto_total_contratos}")
        print(f"Porcentaje promedio de avance: {porcentaje_promedio_avance}")
        print(f"Obra con mayor porcentaje de avance: {obra_mayor_avance.descripcion}")

gestion = GestionarObra()