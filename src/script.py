import pandas as pd 
import seaborn as sns
import kagglehub
import numpy as np
from notebooks.bootcampviztools import (
    plot_combined_graphs,
    pinta_distribucion_categoricas,
    plot_categorical_relationship_fin,
    plot_grouped_boxplots,
    plot_grouped_histograms,
    grafico_dispersion_con_correlacion,
    plot_categorical_numerical_relationship
)
from scipy.stats import pearsonr
def card_tipo(df,umbral_categoria = 10, umbral_continua = 30):
    # Primera parte: Preparo el dataset con cardinalidades, % variación cardinalidad, y tipos
    df_temp = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, df.dtypes]) # Cardinaliad y porcentaje de variación de cardinalidad
    df_temp = df_temp.T # Como nos da los valores de las columnas en columnas, y quiero que estas sean filas, la traspongo
    df_temp = df_temp.rename(columns = {0: "Card", 1: "%_Card", 2: "Tipo"}) # Cambio el nombre de la transposición anterior para que tengan más sentido, y uso asignación en vez de inplace = True (esto es arbitrario para el tamaño de este dataset)

    # Corrección para cuando solo tengo un valor
    df_temp.loc[df_temp.Card == 1, "%_Card"] = 0.00

    # Creo la columna de sugerenica de tipo de variable, empiezo considerando todas categóricas pero podría haber empezado por cualquiera, siempre que adapte los filtros siguientes de forma correspondiente
    df_temp["tipo_sugerido"] = "Categorica"
    df_temp.loc[df_temp["Card"] == 2, "tipo_sugerido"] = "Binaria"
    df_temp.loc[df_temp["Card"] >= umbral_categoria, "tipo_sugerido"] = "Numerica discreta"
    df_temp.loc[df_temp["%_Card"] >= umbral_continua, "tipo_sugerido"] = "Numerica continua"
    # Ojo los filtros aplicados cumplen con el enunciado pero no siguen su orden y planteamiento

    return df_temp


path = kagglehub.dataset_download(
    "amitanshjoshi/spotify-1million-tracks"
)

npath=path+'/spotify_data.csv'
archivo=pd.read_csv(npath, sep=',',index_col=0)
archivo.columns
archivo=archivo[[
        'artist_name', 'track_name', 'track_id', 'popularity', 'genre','year',
        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
        'duration_ms', 'time_signature']]
print(archivo)
pinta_distribucion_categoricas(archivo, ['time_signature'])
grafico_dispersion_con_correlacion(archivo,"year","duration_ms", mostrar_correlacion= True)
df1 = archivo.groupby('year', as_index=False).median(numeric_only=True)
df1=df1.drop(columns=['key','time_signature','mode'])
df1




