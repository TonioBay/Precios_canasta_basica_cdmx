import tabula
import os
import pandas as pd
import fitz

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
pdf_page = pdf[n_pagina] #Lectura de la pagina
area = (306,0,596,150) #Área donde se encuentra la fecha en el pdf (x0 , y0 , x1 , x2)
fecha_texto = pdf_page.get_text("text", clip = area)



df = tables[n_pagina].dropna(axis = 0, how = 'all')
df = df.drop(range(0,2))


def df_list(df):
    """
    Devuelve una lista de dataframes con las columnas necesarias a partir del dataframe original
    """
    n = 1
    #lista con los dataframes
    dfs =[]
    # Lista con los nombres de la central de abasto
    ca_list = ['Tienda de autoservicio', 'Mercados sobreruedas','Mercados publicos','CEDA']
    for i in range(8):
        subdf = pd.DataFrame()
        subdf['Producto'] = df[0] #Columna con el tipo de producto
        if n < 7: # En estas columnas se tiene el dato del precio y la sucursal en la misma casilla, se separa esta columna en dos con su valor correspondiente
            subdf[['Precio','Sucursal']] =df[n].str.split(r'[ \r]', n = 1, expand = True) 
        else:
            subdf['Precio'] = df[n] 
            subdf['Sucursal'] = 'CEDA' # Las columnas de CEDA solo tienen el dato del precio
        if n % 2 == 1 : # columnas impares el costo esta clasificado como bajo
            tipo_costo = 'Bajo'
        else:
            tipo_costo = 'Alto'
        subdf['Canal de abasto'] = ca_list[i//2]
        subdf['Tipo de costo'] = tipo_costo
        n +=1
        dfs.append(subdf)
    return dfs    

dfs = df_list(df)      

df_final = pd.concat(dfs, ignore_index= True)
df_final['Fecha'] = fecha_texto #Columna con la fecha de la pagina
print(df_final)
