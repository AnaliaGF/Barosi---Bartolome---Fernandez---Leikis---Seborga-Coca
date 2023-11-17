from modelo_orm import *
import pandas as pd

pd.set_option('display.float_format', lambda x: '%.2f' % x)
df = pd.read_csv("observatorio-de-obras-urbanas2.csv").replace('­', '', regex=True)

df_entorno = df.sort_values(by=['entorno'])["entorno"].str.upper().unique()

df_etapa = df.sort_values(by=['etapa'])["etapa"].str.upper().unique()

df_monto_contrato = pd.to_numeric(df["monto_contrato"].str.replace('.', '').str.replace(',', '.'), errors='coerce').astype(float)







