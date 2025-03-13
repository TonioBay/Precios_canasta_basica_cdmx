import tabula
import os
import pandas as pd
import fitz
from funciones import fecha, df_list

#Extracción de tablas
ruta_pdf = os.path.join('File', 'ano-2024.pdf')
tables = tabula.read_pdf(
ruta_pdf,
pages = '3',
multiple_tables = True,
lattice= True,
stream = True,
guess = False,
pandas_options= {"header": None}
)
## Extracción de fecha por pagina
n_pagina= 0
pdf = fitz.open(ruta_pdf)
fecha = fecha(pdf,n_pagina)
# Limpieza del dataframe
df = tables[n_pagina].dropna(axis = 0, how = 'all') 
df = df.drop(range(0,2))
## Union de dfs por pagina
dfs = df_list(df)      
df_final = pd.concat(dfs, ignore_index= True)
## Formato por columna
df_final['Fecha'] = fecha #Columna con la fecha de la pagina
df_final['Sucursal'] = df_final['Sucursal'].str.replace(r'[\r\n]', ' ', regex=True) # remplazar valores en columna 'Sucursal'
df_final['Precio'] = df_final['Precio'].str.replace('$','').astype(float) # Eliminación del simbolo en la columna 'Precio' y transformación de string a float
print(df_final)
