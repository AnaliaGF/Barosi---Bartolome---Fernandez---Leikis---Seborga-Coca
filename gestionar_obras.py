from abc import ABC
from modelo_orm import *
import pandas as pd

class GestionarObra(ABC):

    df = pd.DataFrame()
    data = []

    @classmethod
    def extraer_datos(cls):             
        cls.df = pd.read_csv("observatorio-de-obras-urbanas.csv").replace('­', '', regex=True)  

    @classmethod
    def conectar_db(cls):
        db.initialize(SqliteDatabase("obras_urbanas.db"))

    @classmethod
    def mapear_orm(cls):
        db.create_tables([etapa, tipo_obra, tipo_licitacion, area_responsable, barrio, empresa, obra])

    @classmethod
    def limpiar_datos(cls):
        cls.data.append(cls.df["entorno"].str.upper().unique())
        cls.data.append(cls.df["etapa"].str.upper().unique())            

    @classmethod
    def cargar_datos(cls):
        pass

    @classmethod
    def nueva_obra(cls):
        pass

    @classmethod
    def obtener_indicadores(cls):
        pass


gestion = GestionarObra()


gestion.extraer_datos()
gestion.limpiar_datos()
