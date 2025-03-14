import tabula
import os
import pandas as pd
import fitz
from funciones import fecha, df_list
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime

#Extracción de tablas
ruta_pdf = os.path.join('File', 'ano-2024.pdf')
tables = tabula.read_pdf(
ruta_pdf,
pages = 'all',
multiple_tables = True,
lattice= True,
stream = True,
guess = False,
pandas_options= {"header": None}
)
df_final = pd.DataFrame()
dia = 0
for n_pagina in  range(len(tables)):
    
    # Limpieza del dataframe
    df = tables[n_pagina].dropna(axis = 0, how = 'all').reset_index(drop = True)
    df = df.drop(range(0,2)).reset_index(drop = True)
    ## Union de dfs por pagina
    dfs = df_list(df)      
    df_page = pd.concat(dfs, ignore_index= True)
    ## fecha
    try:
        if df_page.iloc[0,0] == 'Aceite Mixto':
            dia += 1
    except: 
        print(f'Página {n_pagina +1} sin datos')
    year = '2024'
    dia_str = str(dia)
    dia_str.rjust(3 + len(dia_str), '0')
    fecha1 =  datetime.strptime(year + "-" + dia_str, "%Y-%j").strftime("%m-%d-%Y")
    df_page['Fecha'] = fecha1 #Columna con la fecha de la pagina
    ## Formato por columna
    df_page['Sucursal'] = df_page['Sucursal'].str.replace(r'[\r\n]', ' ', regex=True) # remplazar valores en columna 'Sucursal'
    df_page['Precio'] = df_page['Precio'].str.replace('$','') # Eliminación del simbolo en la columna 'Precio' 
    df_page = df_page[['Fecha', 'Canal de abasto', 'Sucursal', 'Tipo de costo', 'Producto','Precio']]
    df_final = pd.concat([df_final,df_page], ignore_index= True)
    print(f'Página {n_pagina + 1} procesada')

engine = create_engine("sqlite:///canasta_basica.db")
df_final.to_sql("canasta_basica", engine, if_exists= "append", index = False)
engine.dispose()
df_final.to_csv('canasta_basica.csv', index = False , encoding='latin1')

print('Carga terminada')
