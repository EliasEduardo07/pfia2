import csv
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import googlemaps
import folium
from streamlit_folium import folium_static
import polyline
import streamlit as st

API_KEY = "AIzaSyCRoRdEBeMZUfx_kSjmB-Dgezk2jYWh7bQ"
gmaps = googlemaps.Client(key=API_KEY)

def direccion_a_coordenadas(direccion):
    geocode_result = gmaps.geocode(direccion)
    if geocode_result:
        return geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
    else:
        return None, None

def buscar_supermercados(latitud, longitud, radio):
    supermercados = gmaps.places_nearby(location=(latitud, longitud), radius=radio, type='supermarket')['results']
    return supermercados

def calcular_distancia_manhattan(coordenadas1, coordenadas2):
    latitud1, longitud1 = coordenadas1
    latitud2, longitud2 = coordenadas2
    return abs(latitud1 - latitud2) + abs(longitud1 - longitud2)
 
def calcular_distancia_euclidiana(coordenadas1, coordenadas2):
    latitud1, longitud1 = coordenadas1
    latitud2, longitud2 = coordenadas2
    return ((latitud1 - latitud2) ** 2 + (longitud1 - longitud2) ** 2) ** 0.5

def calcular_ruta(latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    directions_result = gmaps.directions((latitud_origen, longitud_origen),
                                         (latitud_destino, longitud_destino),
                                         mode="driving")
    return directions_result

def app():
    st.title("Metricas de distancia")

    ubicacion_usuario = st.text_input("Por favor ingresa tu ubicación (ejemplo: 'Ciudad de México'):")

    if ubicacion_usuario:
        latitud_actual, longitud_actual = direccion_a_coordenadas(ubicacion_usuario)

        if latitud_actual and longitud_actual:
            st.write("Tu ubicación actual: {}, {}".format(latitud_actual, longitud_actual))
            radio_busqueda = st.number_input("Ingrese             radio de búsqueda en metros:", min_value=100)

            supermercados_cercanos = buscar_supermercados(latitud_actual, longitud_actual, radio_busqueda)
            supermercados_y_distancias = []

            for supermercado in supermercados_cercanos:
                nombre = supermercado['name']
                direccion = supermercado['vicinity']
                coordenadas_supermercado = supermercado['geometry']['location']
                latitud_supermercado = coordenadas_supermercado['lat']
                longitud_supermercado = coordenadas_supermercado['lng']

                distancia_manhattan = calcular_distancia_manhattan((latitud_actual, longitud_actual), (latitud_supermercado, longitud_supermercado))
                distancia_euclidiana = calcular_distancia_euclidiana((latitud_actual, longitud_actual), (latitud_supermercado, longitud_supermercado))

                supermercados_y_distancias.append((nombre, distancia_manhattan, distancia_euclidiana, latitud_supermercado, longitud_supermercado))

            supermercados_y_distancias.sort(key=lambda x: x[2])

            st.subheader("Distancias de supermercados cercanos:")
            opciones_supermercados = [nombre for nombre, _, _, _, _ in supermercados_y_distancias]
            supermercado_seleccionado = st.selectbox("Seleccione un supermercado:", opciones_supermercados)

            for nombre, distancia_manhattan, distancia_euclidiana, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                if nombre == supermercado_seleccionado:
                    st.write("Nombre: ", nombre)
                    st.write("Distancia Manhattan: ", distancia_manhattan)
                    st.write("Distancia Euclidiana: ", distancia_euclidiana)
                    break

            mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
            folium.Marker([latitud_actual, longitud_actual], popup='Ubicación actual', icon=folium.Icon(color='blue')).add_to(mapa)
            for nombre, _, _, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                folium.Marker([latitud_supermercado, longitud_supermercado], popup=nombre, icon=folium.Icon(color='red')).add_to(mapa)
            folium_static(mapa)

            if st.button("Calcular ruta"):
                for nombre, _, _, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                    if nombre == supermercado_seleccionado:
                        ruta = calcular_ruta(latitud_actual, longitud_actual, latitud_supermercado, longitud_supermercado)
                        break
                if ruta:
                    ruta_mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
                    folium.PolyLine([(step['start_location']['lat'], step['start_location']['lng']) for step in ruta[0]['legs'][0]['steps']], color="green", weight=2.5, opacity=1).add_to(ruta_mapa)
                    folium_static(ruta_mapa)
                else:
                    st.write("No se pudo calcular la ruta.")
        else:
            st.write("No se pudo obtener la ubicación a partir de la dirección ingresada. Por favor intente con otra dirección.")
    else:
        st.write("Por favor ingrese su ubicación para continuar.")

if __name__ == "__main__":
    app()

