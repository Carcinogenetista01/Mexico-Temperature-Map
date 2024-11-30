import streamlit as st
import geopandas as gpd
import plotly.express as px
import json
import numpy as np
from datetime import datetime
import os

# Wrap your Streamlit app with Flask
def main():
    st.set_page_config(page_title="Mapa de Temperatura de México", page_icon="🌡️", layout="wide")
    port = int(os.environ.get("PORT", 8080))
# Estilos CSS personalizados
    st.markdown("""
    <style>
        :root {
            --primary-color: #3498DB;
            --background-color: #F0F4F8;
            --text-color: #2C3E50;
            --card-background: #FFFFFF;
        }
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2980B9;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stSelectbox, .stDateInput {
            background-color: var(--card-background);
            border-radius: 5px;
            border: 1px solid #E5E7EB;
            padding: 5px;
        }
        .stRadio>div {
            background-color: var(--card-background);
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --primary-color: #4299E1;
                --background-color: #1A202C;
                --text-color: #E2E8F0;
                --card-background: #2D3748;
            }
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    main()
@st.cache_data
# Función auxiliar para obtener la ruta del archivo
def get_file_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

@st.cache_data
def load_estados_geojson():
    file_path = get_file_path('mexicoHigh.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        estados_geojson = json.load(file)
        gdf_estados = gpd.GeoDataFrame.from_features(estados_geojson['features'])
        gdf_estados = gdf_estados.set_crs(epsg=4326, inplace=True)
        gdf_estados['temperatura'] = np.random.uniform(10, 35, len(gdf_estados))
        return gdf_estados

st.markdown("""
    <h1 style='text-align: center; color: #3498DB; animation: fadeIn 2s;'>
        🌡️ Mapa de Temperatura de México
    </h1>
    <style>
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        .decoration {
            background: linear-gradient(45deg, #3498DB, #2980B9);
            height: 5px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_clima_data():
    file_path = get_file_path('ClimaOut.json')
    with open(file_path, 'r') as file:
        clima_data = json.load(file)
    return clima_data

@st.cache_data
def load_estados_data():
    file_path = get_file_path('AtrOut.json')
    with open(file_path, 'r') as file:
        estados_data = json.load(file)['atrClean']
    return {estado['ides']: estado['nes'] for estado in estados_data}

@st.cache_data
def load_municipios_data():
    file_path = get_file_path('munOut.json')
    with open(file_path, 'r') as file:
        municipios_data = json.load(file)
    return municipios_data


@st.cache_data
def load_geojson_data():
    file_path = get_file_path('municipios_limpios.geojson')
    with open(file_path, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

    # Renombrar las columnas para que coincidan con lo que esperamos
    gdf = gdf.rename(columns={
        'id_estado': 'NAME_1',
        'nombre_municipio': 'NAME_2',
        'id_municipio': 'ID_2'
    })

    # Asegurarse de que tengamos una columna de geometría
    if 'geometry' not in gdf.columns:
        st.error("No se encontró una columna de geometría en el GeoDataFrame")
        return None

    # Establecer el sistema de coordenadas
    gdf = gdf.set_crs(epsg=4326, inplace=True)

    # Verificar y corregir la geometría si es necesario
    gdf['geometry'] = gdf['geometry'].make_valid()

    # Calcular centroides para cada geometría
    gdf['centroid'] = gdf['geometry'].centroid

    # Extraer latitud y longitud del centroide
    gdf['latitude'] = gdf['centroid'].y
    gdf['longitude'] = gdf['centroid'].x

    # Añadir una columna de temperatura aleatoria
    gdf['temperatura'] = np.random.uniform(15, 35, len(gdf))

    return gdf

# Uso de la función
try:
    with st.spinner('Cargando datos geoespaciales...'):
        gdf = load_geojson_data()
    if gdf is not None:
        st.success('Datos geoespaciales cargados correctamente')
        
        # Mostrar las primeras filas del GeoDataFrame
        st.write("Primeras filas del GeoDataFrame:")
        st.write(gdf.head())
        
        # Mostrar información sobre el CRS
        st.write(f"Sistema de Coordenadas de Referencia (CRS): {gdf.crs}")

        # Mostrar las columnas disponibles
        st.write("Columnas disponibles en el GeoDataFrame:")
        st.write(gdf.columns.tolist())
    else:
        st.error("No se pudieron cargar los datos geoespaciales correctamente")
except Exception as e:
    st.error(f"Error al cargar los datos geoespaciales: {str(e)}")
    st.stop()
# Carga de datos
with st.spinner('Cargando datos...'):
    gdf = load_geojson_data()

def get_center_and_zoom(gdf, nivel, selected_area=None, selected_municipio=None):
    if nivel == 'General':
        return {"lat": 23.6345, "lon": -102.5528}, 4
    elif nivel == 'Estado':
        area_gdf = gdf[gdf['NAME_1'] == selected_area]
        bounds = area_gdf.total_bounds
        return {"lat": (bounds[1] + bounds[3]) / 2, "lon": (bounds[0] + bounds[2]) / 2}, 6
    else:
        mun_gdf = gdf[(gdf['NAME_1'] == selected_area) & (gdf['NAME_2'] == selected_municipio)]
        centroid = mun_gdf.geometry.centroid.iloc[0]
        return {"lat": centroid.y, "lon": centroid.x}, 8


# Carga de datos
with st.spinner('Cargando datos...'):
    gdf = load_geojson_data()

# Inicializar variables
selected_state = None
selected_municipio = None

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Configuración")

    nivel = st.radio("📊 Nivel de visualización:", ('General', 'Estado', 'Municipio'))

    gdf_estados = load_estados_geojson()
    temp_mexico = gdf_estados['temperatura'].mean()

    if nivel != 'General':
        selected_state = st.selectbox("🏙️ Selecciona un estado", sorted(gdf['NAME_1'].unique()))

        if nivel == 'Municipio':
            municipios = sorted(gdf[gdf['NAME_1'] == selected_state]['NAME_2'].unique())
            selected_municipio = st.selectbox("🏘️ Selecciona un municipio", [''] + municipios)


    with st.spinner('Calculando estadísticas...'):
        # Filter and aggregate data according to the selection
        if nivel == 'General':
            filtered_gdf = gdf_estados
            hover_name = 'name'
        elif nivel == 'Estado' and selected_state:
            filtered_gdf = gdf[gdf['NAME_1'] == selected_state]
            hover_name = 'NAME_2'
        elif nivel == 'Municipio' and selected_state:
            filtered_gdf = gdf[gdf['NAME_1'] == selected_state]
            if selected_municipio:
                filtered_gdf = filtered_gdf[filtered_gdf['NAME_2'] == selected_municipio]
            hover_name = 'NAME_2'
        else:
            filtered_gdf = gdf
            hover_name = 'NAME_2'
            st.markdown("#### ���️ Temperaturas")
        col_stats1, col_stats2 = st.columns(2)

        with col_stats1:
            st.markdown("#### 🌡️ Temperaturas")
            temp_min = filtered_gdf['temperatura'].min()
            temp_max = filtered_gdf['temperatura'].max()
            temp_avg = filtered_gdf['temperatura'].mean()

            st.metric("Temperatura mínima", f"{temp_min:.1f}°C")
            st.metric("Temperatura máxima", f"{temp_max:.1f}°C")
            st.metric("Temperatura promedio", f"{temp_avg:.1f}°C")

        with col_stats2:
            st.markdown("#### 🏙️ Datos geográficos")
            num_municipios = len(filtered_gdf)
            st.metric("Número de municipios", num_municipios)

        # Dashboard de Temperaturas Mínimas por EstadoMáximas por Municipio
        st.markdown("### 🌡️ Dashboard de Temperaturas Máximas por Municipio")

        # Selección de estado y fecha
        col_estado, col_fecha = st.columns(2)
        with col_estado:
            estado_dashboard = st.selectbox("Selecciona un estado para el dashboard:",
                                            [''] + sorted(gdf['NAME_1'].unique()),
                                            key='estado_dashboard')
        with col_fecha:
            fecha_dashboard = st.date_input("Selecciona una fecha:", key='fecha_dashboard')

        if estado_dashboard and fecha_dashboard:
            with st.spinner('Generando dashboard de temperaturas máximas...'):
                # Filtrar datos para el estado seleccionado
                df_estado = gdf[gdf['NAME_1'] == estado_dashboard]

                # Simular datos de temperatura máxima para cada municipio
                df_estado['tmax'] = np.random.uniform(25, 40, len(df_estado))

                # Ordenar municipios por temperatura máxima de mayor a menor
                df_estado_sorted = df_estado.sort_values('tmax', ascending=False)

                # Mostrar los primeros 15 municipios
                top_15 = df_estado_sorted.head(15)

                # Crear gráfico de barras
                fig_tmax = px.bar(
                    top_15,
                    x='NAME_2',
                    y='tmax',
                    title=f'Top 15 Municipios con Mayor Temperatura Máxima en {estado_dashboard} ({fecha_dashboard})',
                    labels={'NAME_2': 'Municipio', 'tmax': 'Temperatura Máxima (°C)'}
                )

                # Mostrar datos en una tabla
                st.write("Datos de Temperatura Máxima:")
                st.dataframe(top_15[['NAME_2', 'tmax']])
                st.plotly_chart(fig_tmax, use_container_width=True)
                fig_tmax.update_layout(xaxis_tickangle=-30)





if nivel == 'Estado' and selected_state:
    temp = gdf[gdf['NAME_1'] == selected_state]['temperatura'].mean()
    st.metric(label=f"🌡️ Temperatura promedio en {selected_state}", value=f"{temp:.1f}°C")
elif nivel == 'Municipio' and selected_state:
    if selected_municipio:
        temp = gdf[(gdf['NAME_1'] == selected_state) & (gdf['NAME_2'] == selected_municipio)]['temperatura'].values[0]
        st.metric(label=f"🌡️ Temperatura en {selected_municipio}, {selected_state}", value=f"{temp:.1f}°C")
    else:
        temp = gdf[gdf['NAME_1'] == selected_state]['temperatura'].mean()
        st.metric(label=f"🌡️ Temperatura promedio en {selected_state}", value=f"{temp:.1f}°C")

# Initialize selected_datetime with the current date and time
selected_datetime = datetime.now()

# Mostrar información adicional si se ha seleccionado un estado
if selected_state:
    total_municipios = gdf[gdf['NAME_1'] == selected_state]['NAME_2'].nunique()
    st.info(f"📊 Total de municipios en {selected_state}: {total_municipios}")

    st.markdown("### ⏰ Línea de Tiempo")
    selected_date = st.date_input("Fecha:", datetime.now().date())
    selected_hour = st.time_input("Hora:", datetime.now().time())
    selected_datetime = datetime.combine(selected_date, selected_hour)

    # Elemento decorativo
    st.markdown("<div class='decoration'></div>", unsafe_allow_html=True)

# Display the selected datetime (now this will always be defined)
st.markdown("Datos actualizados al: " + str(selected_datetime))

st.markdown("</div>", unsafe_allow_html=True)

# Modificar la parte de filtrado y creación del mapa
with col2:
    st.markdown("### 🗺️ Mapa de Temperatura")

    try:
        # Get the center and zoom of the map
        center, zoom = get_center_and_zoom(gdf, nivel, selected_state, selected_municipio)

        # Filter and aggregate data according to the selection
        if nivel == 'General':
            filtered_gdf = gdf_estados
            hover_name = 'name'
        elif nivel == 'Estado' and selected_state:
            filtered_gdf = gdf[gdf['NAME_1'] == selected_state]
            hover_name = 'NAME_2'
        elif nivel == 'Municipio' and selected_state:
            filtered_gdf = gdf[gdf['NAME_1'] == selected_state]
            if selected_municipio:
                filtered_gdf = filtered_gdf[filtered_gdf['NAME_2'] == selected_municipio]
            hover_name = 'NAME_2'
        else:
            filtered_gdf = gdf
            hover_name = 'NAME_2'

        # Create the map
        fig = px.choropleth_mapbox(
            filtered_gdf,
            geojson=filtered_gdf.geometry,
            locations=filtered_gdf.index,
            color='temperatura',
            color_continuous_scale="RdYlBu_r",
            range_color=[15, 35],
            mapbox_style="carto-positron",
            zoom=zoom,
            center=center,
            opacity=0.5,
            labels={'temperatura': 'Temperatura (°C)'},
            hover_name=hover_name,
            hover_data={'temperatura': ':.1f'}
        )
        
        # Actualizar el diseño del mapa y la etiqueta emergente
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=center,
                zoom=zoom,
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=600,
            hoverlabel=dict(
                bgcolor="rgba(255, 255, 255, 0.8)",  # Fondo blanco semi-transparente
                font_size=14,  # Tamaño de fuente más grande
                font_family="Arial",  # Fuente fácil de leer
                font_color="#333333",  # Color de texto oscuro
                bordercolor="#666666",  # Borde gris oscuro
                align="left",  # Alineación del texto a la izquierda
            )
        )
        
        # Ocultar la leyenda de los trazos
        fig.update_traces(showlegend=False)

        # Mostrar el mapa
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error al generar el mapa: {str(e)}")

        # Gráfico de distribución de temperaturas
        st.markdown("### 📈 Distribución de Temperaturas")

    with st.spinner('Generando histograma...'):
        fig_hist = px.histogram(
        filtered_gdf,
        x='temperatura',
        nbins=20,
        labels={'temperatura': 'Temperatura (°C)', 'count': 'Frecuencia'},
        title='Distribución de Temperaturas',
        width=800,
        height=400
    )


st.write("Por favor, selecciona un estado y una fecha para ver el dashboard.")
st.markdown("---")
st.markdown("Desarrollado con ❤️ por Abril Montaño")
st.markdown("© 2023 Mapa de Temperatura de México. Todos los derechos reservados.")
