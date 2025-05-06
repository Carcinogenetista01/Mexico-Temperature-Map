# 🌡️ Mapa de Temperatura de México

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GeoPandas](https://img.shields.io/badge/GeoPandas-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Aplicación web interactiva que visualiza temperaturas en México a diferentes niveles geográficos (nacional, estatal y municipal) utilizando Streamlit, GeoPandas y Plotly.

## 🚀 Características principales

- **Visualización jerárquica**: Navega entre vistas generales de todo México, por estado o por municipio
- **Datos interactivos**: 
  - Mapa coroplético con escala de colores para temperaturas
  - Gráficos de distribución de temperaturas
  - Dashboard de temperaturas máximas por municipio
- **Estadísticas en tiempo real**: 
  - Temperaturas mínimas, máximas y promedio
  - Conteo de municipios por área seleccionada
- **Diseño responsive**: Adaptable a diferentes dispositivos con modo claro/oscuro
- **Filtros avanzados**: 
  - Selección por fecha y hora
  - Navegación por niveles geográficos

## 📦 Requisitos

- Python 3.8+
- Streamlit
- GeoPandas
- Plotly
- NumPy
- Requests

Instala las dependencias con:
```bash
pip install -r requirements.txt
```

## 🛠️ Configuración

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/mapa-temperatura-mexico.git
cd mapa-temperatura-mexico
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

## 🗺️ Estructura de archivos

```
├── app.py                # Aplicación principal
├── ClimaOut.json         # Datos climáticos
├── AtrOut.json           # Atributos de estados
├── munOut.json           # Datos de municipios
├── municipios_limpios.geojson  # Datos geoespaciales
└── README.md
```

## 📊 Funcionamiento

La aplicación carga datos geoespaciales de México y los combina con datos de temperatura simulados. Los usuarios pueden:

1. Seleccionar el nivel de visualización (General, Estado o Municipio)
2. Filtrar por estado y municipio
3. Ver estadísticas de temperatura
4. Explorar el mapa interactivo
5. Analizar distribuciones de temperatura

## 🌟 Contribuciones

¡Las contribuciones son bienvenidas! Por favor abre un issue o envía un pull request para:

- Mejorar la visualización de datos
- Añadir datos reales de temperatura
- Implementar nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

Desarrollado con ❤️ por Abril Montaño  
© 2023 Mapa de Temperatura de México
