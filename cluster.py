import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

# Cargar datos
@st.cache_data()
def load_data():
    data = pd.read_csv('datos.csv')  # Reemplaza 'datos.csv' con el nombre de tu archivo de datos
    return data

# Realizar clustering ascendente
def clustering_ascendente(data, n_clusters):
    clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    clusters = clustering.fit_predict(data)
    return clusters

# Mostrar resultados del clustering
def mostrar_resultados(data, clusters):
    # Mapa de calor
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(data, cmap='viridis', cbar=False, ax=ax)
    ax.set_xlabel('Características')
    ax.set_ylabel('Alimentos')
    ax.set_title('Mapa de Calor: Distribución de Características')
    st.pyplot(fig)
    st.write("El mapa de calor muestra la distribución de las características en los alimentos. Los colores más oscuros indican valores más altos.")

    # Dendrograma
    fig, ax = plt.subplots(figsize=(8, 6))
    dendrogram(linkage(data, method='ward'))
    ax.set_xlabel('Alimentos')
    ax.set_ylabel('Distancia')
    ax.set_title('Dendrograma: Estructura Jerárquica')
    st.pyplot(fig)
    st.write("El dendrograma muestra la estructura jerárquica del clustering ascendente. Las ramas del dendrograma representan la similitud entre los alimentos.")

    # Scatter plot con clusters
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(data['Proteinas'], data['Carbohidratos'], c=clusters, cmap='viridis')
    legend = ax.legend(*scatter.legend_elements(), title='Clusters')
    ax.add_artist(legend)
    ax.set_xlabel('Proteínas')
    ax.set_ylabel('Carbohidratos')
    ax.set_title('Scatter Plot: Clusters')
    st.pyplot(fig)
    st.write("El scatter plot muestra la distribución de los alimentos en el espacio de las proteínas y los carbohidratos. Cada punto representa un alimento y se colorea de acuerdo al cluster al que pertenece.")

    # Análisis de clusters
    cluster_analysis = pd.DataFrame({'Alimento': data.index, 'Cluster': clusters})
    cluster_counts = cluster_analysis['Cluster'].value_counts().sort_index()
    st.subheader("Análisis de Clusters")
    st.write(cluster_counts)
    st.write("El análisis de clusters muestra la cantidad de alimentos en cada cluster. Esto nos proporciona una idea de la distribución de los alimentos en los diferentes grupos.")

    # Análisis de cada cluster
    st.subheader("Análisis de cada Cluster")
    for cluster_id in range(len(cluster_counts)):
        cluster_data = cluster_analysis[cluster_analysis['Cluster'] == cluster_id]
        st.write(f"Cluster {cluster_id + 1}:")
        st.write(cluster_data)


def main():
    # Cargar datos
    data = load_data()

    # Mostrar datos
    st.subheader("Datos")
    st.write(data)

    # Parámetros del clustering
    n_clusters = st.slider("Selecciona el número de Clusters", min_value=2, max_value=10, value=3)

    # Realizar clustering ascendente
    clusters = clustering_ascendente(data[['Proteinas', 'Carbohidratos']], n_clusters)

    # Mostrar resultados
    st.subheader("Resultados del Clustering")
    mostrar_resultados(data[['Proteinas', 'Carbohidratos']], clusters)

if __name__ == '__main__':
    main()
