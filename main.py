import tabula
import pandas as pd
from decouple import config

ruta_pdf = config('RUTA_PDF')
tables = tabula.read_pdf(
ruta_pdf,
pages = '2-3',
multiple_tables = True,
lattice= True,
stream = True,
guess = False,
pandas_options= {"header": None}
)

df = tables[1].dropna(axis = 0, how = 'all')
df = df.drop(range(0,2))

def df_list(df):
    """
    Devuelve una lista de dataframes con las columnas necesarias a partir del dataframe original
    """
    n = 1
    dfs =[]
    for i in range(8):
        subdf = pd.DataFrame()
        subdf['Producto'] = df[0]
        if n < 7:
            subdf[['Precio','Sucursal']] =df[n].str.split(r'[ \r]', n = 1, expand = True)
        else:
            subdf['Precio'] = df[n] 
            subdf['Sucursal'] = 'CEDA'
        if n % 2 == 1 :
            tipo_costo = 'Bajo'
        else:
            tipo_costo = 'alto'
        subdf['Tipo de costo'] = tipo_costo
        n +=1
        #print(subdf)
        dfs.append(subdf)
    return dfs    

dfs = df_list(df)      

df_final = pd.concat(dfs, ignore_index= True)
     
print(df_final)
