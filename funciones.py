import pandas as pd
import fitz
import locale
from datetime import datetime
import numpy as np

def fecha(pdf,n_pagina):
    """
    Devuelve la fecha de una pagina en formato datetime
    """
    locale.setlocale(locale.LC_TIME,'es_ES.UTF-8') # formato de fecha en español
    pdf_page = pdf[n_pagina] #Lectura de la pagina
    
    if n_pagina < 84:
        x0 , y0 , x1, y1 = 306,0,596,150
    elif n_pagina < 580 :
        x0 , y0 , x1, y1 = 362,0,596,175
    elif n_pagina < 582:
        x0 , y0 , x1, y1 = 362,0,596,121
    else:
        x0 , y0 , x1, y1 = 362,0,596,134        
    area = (x0 , y0 , x1, y1) #Área donde se encuentra la fecha en el pdf (x0 , y0 , x1 , x2)
    fecha_texto = pdf_page.get_text("text", clip = area)
    fecha_format = fecha_texto.replace(' ','').replace('de','-').strip()
    fecha = datetime.strptime(fecha_format,'%d-%B-%Y').date() #String a datetime
    return fecha

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
            try:
                subdf[['Precio','Sucursal']] =df[n].str.split(r'[ \r]', n = 1, expand = True) 
            except: 
                subdf['Precio'] =df[n]
                subdf['Sucursal'] = np.nan
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