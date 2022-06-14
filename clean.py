import pandas as pd
import json
import gspread
from main import _create_dataframe

def clean():
    df = pd.read_csv('raw_dataset.csv')
    df = df.iloc[:,1:]

    df['features'] = df['features'].str.replace("'",'"')
    df['features'] = df['features'].str.replace(" ",'')
    df['features'] = df['features'].apply(lambda x: json.loads(x))
    count=0
    for row in df['features']:
        row.update({'key': count})
        count +=1
    features_list = []
    for row in df['features']:
        features_list.append(row)
    df2 = pd.DataFrame(features_list)

    df['key'] = df.index
    df_final = df.merge(df2, on='key',how='left')
    df_final.drop(columns = ['key','features'], inplace=True)

    df_final['title'] = df_final['title'].str.replace(r' #[0-9]+.*$','',regex=True)
    df_final['modelo'] = df_final['title'].str.extract(r'(\s\d+$)')
    df_final['title'] = df_final['title'].str.replace(r'\s\d+$','',regex=True)
    df_final['brand'] = df_final['title'].str.extract(r'(^[A-Z-a-z]+) .*')

    df_final['km'] = df_final['km'].str.replace(r'\D','',regex=True)
    df_final['price'] = df_final['price'].str.replace(r'\D','',regex=True)

    df_final = df_final[['StockID','title','brand','modelo','Transmisión','km','price','url','image_link']]

    df_final = df_final.fillna('')
    df_final = df_final.drop_duplicates()
    df_final = df_final.rename(columns={
    'StockID' : 'Stock Id',
    'title' : 'Automovil',
    'brand' : 'Marca',
    'modelo' : 'Modelo (Año)',
    'km' : 'Kilometraje',
    'price' : 'Precio',
    'url' : 'URL',
    'image_link' : 'URL de la Imagen'

})
    return df_final
if __name__ == '__main__':
    clean()