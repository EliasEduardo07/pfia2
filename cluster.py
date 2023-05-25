import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.impute import SimpleImputer

# Cargar datos
@st.cache_data()
def load_data():
    data = pd.read_csv('datos.csv')  # Reemplaza 'datos.csv' con el nombre de tu archivo de datos
    
    # Convertir columnas a numéricas
    data['Grasas'] = pd.to_numeric(data['Grasas'], errors='coerce')
    data['Vitaminas'] = pd.to_numeric(data['Vitaminas'], errors='coerce')
    data['Minerales'] = pd.to_numeric(data['Minerales'], errors='coerce')
    data['Calorias'] = pd.to_numeric(data['Calorias'], errors='coerce')
    
    return data

def clustering_ascendente(data, n_clusters):
    clustering = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
    clusters = clustering.fit_predict(data)
    return clusters

def interpretar_cluster(cluster):
    if cluster == 0:
        return 'Alimentos ricos en grasas'
    elif cluster == 1:
        return 'Alimentos ricos en proteínas'
    elif cluster == 2:
        return 'Alimentos ricos en carbohidratos'
    elif cluster == 3:
        return 'Alimentos con vitaminas y minerales'
    elif cluster == 4:
        return 'Alimentos con calorías moderadas'
    elif cluster == 5:
        return 'Alimentos con alta densidad de nutrientes'
    elif cluster == 6:
        return 'Alimentos bajos en carbohidratos y grasas'
    elif cluster == 7:
        return 'Alimentos con alta cantidad de proteínas'
    elif cluster == 8:
        return 'Alimentos con nutrientes equilibrados'
    else:
        return 'Alimentos con perfil nutricional variado'

def main():
    # Cargar datos
    data = load_data()
    
    # Imputar valores faltantes en cada columna
    columns_to_impute = ['Proteinas', 'Carbohidratos', 'Grasas', 'Vitaminas', 'Minerales', 'Calorias']
    for column in columns_to_impute:
        imputer = SimpleImputer(strategy='mean')
        data[column] = imputer.fit_transform(data[[column]])
    
    # Número de clusters
    n_clusters = st.slider('Selecciona el número de clusters:', 2, 10, 3)
    
    # Clustering ascendente
    clusters = clustering_ascendente(data[['Proteinas', 'Carbohidratos', 'Grasas', 'Vitaminas', 'Minerales', 'Calorias']], n_clusters)
    
    # Mapa de calor
    st.subheader('Mapa de Calor')
    fig, ax = plt.subplots()
    sns.heatmap(data[['Proteinas', 'Carbohidratos', 'Grasas', 'Vitaminas', 'Minerales', 'Calorias']].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    
    # Dendrograma
    st.subheader('Dendrograma')
    fig, ax = plt.subplots(figsize=(10, 6))
    dendrogram(linkage(data[['Proteinas', 'Carbohidratos', 'Grasas', 'Vitaminas', 'Minerales', 'Calorias']], method='ward'), ax=ax)
    st.pyplot(fig)
    
    # Mostrar clusters y alimentos por cluster
    st.subheader('Clusters')
    for cluster in range(n_clusters):
        st.write(f'**Cluster {cluster + 1}:** {interpretar_cluster(cluster)}')
        alimentos = data[clusters == cluster]['Alimento']
        st.write(alimentos.tolist())

if __name__ == '__main__':
    main()
