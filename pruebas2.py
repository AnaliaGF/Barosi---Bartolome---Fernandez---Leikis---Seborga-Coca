from modelo_orm import *
import pandas as pd


db.initialize(SqliteDatabase("obras_urbanas.db"))
db.create_tables([etapa, tipo_obra, tipo_licitacion, area_responsable, barrio, empresa, obra])


pd.set_option('display.float_format', lambda x: '%.2f' % x)
df = pd.read_csv("observatorio-de-obras-urbanas2.csv").replace('­', '', regex=True)

#df_entorno = df.sort_values(by=['entorno'])["entorno"].str.upper().unique()

#df_etapa = df.sort_values(by=['etapa'])["etapa"].str.upper().unique()

#df_monto_contrato = pd.to_numeric(df["monto_contrato"].str.replace('.', '').str.replace(',', '.'), errors='coerce').astype(float)

df_barrio = df[["comuna", "barrio"]]
df_barrio_unico = pd.unique(df_barrio)

#.sort_values(by=['barrio'])
lalala = df_barrio



