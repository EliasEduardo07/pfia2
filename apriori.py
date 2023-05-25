import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def cargar_datos():
    # Cargar datos desde el archivo CSV sin nombres de columna
    datos = pd.read_csv("ingredientes.csv", header=None)
    return datos

def encontrar_reglas_asociacion(datos, ingrediente1, ingrediente2, confianza, soporte, elevacion):
    # Combinar las columnas en una sola lista por fila
    transacciones = datos.apply(lambda row: row.dropna().tolist(), axis=1).tolist()

    # Preparar datos para el algoritmo Apriori
    te = TransactionEncoder()
    te_transacciones = te.fit(transacciones).transform(transacciones)
    df_transacciones = pd.DataFrame(te_transacciones, columns=te.columns_)

    # Ejecutar algoritmo Apriori con los valores seleccionados
    frecuentes = apriori(df_transacciones, min_support=soporte, use_colnames=True)
    reglas = association_rules(frecuentes, metric="confidence", min_threshold=confianza)
    reglas_filtradas = reglas[reglas['lift'] > elevacion]

    return reglas_filtradas

def graficar_frecuencia(datos):
    # Filtrar los valores con espacios en blanco
    datos_filtrados = datos.apply(lambda x: x[x != ""], axis=1)

    # Obtener la frecuencia de los ingredientes
    ingredientes_frecuencia = datos_filtrados.unstack().value_counts()

    # Filtrar los ingredientes con frecuencia mayor a 1
    ingredientes_frecuencia = ingredientes_frecuencia[ingredientes_frecuencia > 1]

    # Crear gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=ingredientes_frecuencia.values, y=ingredientes_frecuencia.index)
    plt.xlabel("Frecuencia")
    plt.ylabel("Ingrediente")
    plt.title("Frecuencia de los Ingredientes")
    st.pyplot(fig)

def main():
    # Título de la aplicación
    st.title("Nutria AI - Apriori")

    # Cargar datos
    datos = cargar_datos()

    # Solicitar ingredientes al usuario
    ingrediente1 = st.text_input("Ingrediente 1", max_chars=50).strip().lower()
    ingrediente2 = st.text_input("Ingrediente 2", max_chars=50).strip().lower()

    # Barras deslizantes para los valores de confianza, soporte y elevación
    confianza = st.slider("Confianza", min_value=0.0, max_value=1.0, step=0.1, value=0.5)
    soporte = st.slider("Soporte", min_value=0.0, max_value=1.0, step=0.1, value=0.1)
    elevacion = st.slider("Elevación", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

    # Botón para generar la interpretación y la gráfica de frecuencias
    if st.button("Generar Interpretación y Gráfica de Frecuencias"):
        if ingrediente1 and ingrediente2:
            # Encontrar reglas de asociación
            reglas = encontrar_reglas_asociacion(datos, ingrediente1, ingrediente2, confianza, soporte, elevacion)

            if reglas.empty:
                st.write("No se encontraron reglas de asociación para los ingredientes seleccionados.")
            else:
                st.write("Reglas de asociación encontradas:")
                st.dataframe(reglas)

                # Explicación de las reglas de asociación
                st.subheader("Explicación de las reglas de asociación:")
                st.write("Las reglas de asociación encontradas muestran patrones comunes entre los ingredientes.")
                st.write("Cada regla consta de dos partes: el antecedente (ingredientes previos) y el consecuente (ingrediente siguiente).")
                st.write("La confianza indica la probabilidad de que el consecuente esté presente dado el antecedente.")
                st.write("Un valor de confianza alto significa que el ingrediente consecuente se encuentra con frecuencia después del antecedente.")
                st.write("La elevación indica la fuerza de la asociación entre el antecedente y el consecuente.")
                st.write("Un valor de elevación alto significa que la aparición del antecedente aumenta significativamente la probabilidad de que aparezca el consecuente.")

                # Sugerencias de ingredientes
                st.subheader("Ejemplo de interpretación:")
                st.write(f"Si el usuario selecciona '{ingrediente1}' y '{ingrediente2}' como ingredientes, las reglas de asociación pueden proporcionar sugerencias como:")

                sugerencias = []
                for _, regla in reglas.iterrows():
                    antecedente = ", ".join(f"**{ingrediente}**" if ingrediente in [ingrediente1, ingrediente2] else ingrediente for ingrediente in regla["antecedents"])
                    consecuente = ", ".join(f"**{ingrediente}**" if ingrediente in [ingrediente1, ingrediente2] else ingrediente for ingrediente in regla["consequents"])
                    sugerencias.append(f"Si tienes {antecedente}, es probable que también tengas {consecuente}.")

                for sugerencia in sugerencias:
                    st.write(f"- {sugerencia}")

            # Graficar frecuencia de los ingredientes
            graficar_frecuencia(datos)

if __name__ == "__main__":
    main()
