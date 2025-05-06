# 🌡️ Mexico Temperature Map

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GeoPandas](https://img.shields.io/badge/GeoPandas-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Interactive web application that visualizes temperature data across Mexico at different geographic levels (national, state, and municipal) using Streamlit, GeoPandas, and Plotly.

## 🚀 Key Features

- **Hierarchical visualization**: Navigate between country-wide, state-level, or municipal views
- **Interactive data**:
  - Choropleth map with temperature color scale
  - Temperature distribution charts
  - Municipal maximum temperature dashboard
- **Real-time statistics**:
  - Minimum, maximum, and average temperatures
  - Municipality counts by selected area
- **Responsive design**: Adapts to different devices with light/dark mode
- **Advanced filters**:
  - Date and time selection
  - Geographic level navigation

## 📦 Requirements

- Python 3.8+
- Streamlit
- GeoPandas
- Plotly
- NumPy
- Requests

Install dependencies with:
```bash
pip install -r requirements.txt
```

## 🛠️ Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/mexico-temperature-map.git
cd mexico-temperature-map
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 🗺️ File Structure

```
├── app.py                # Main application
├── ClimaOut.json         # Climate data
├── AtrOut.json           # State attributes
├── munOut.json           # Municipal data
├── municipios_limpios.geojson  # Geospatial data
└── README.md
```

## 📊 How It Works

The application loads geospatial data of Mexico combined with simulated temperature data. Users can:

1. Select visualization level (Country, State, or Municipality)
2. Filter by state and municipality
3. View temperature statistics
4. Explore the interactive map
5. Analyze temperature distributions

## 🌟 Contributions

Contributions are welcome! Please open an issue or submit a pull request for:

- Improving data visualization
- Adding real temperature data
- Implementing new features

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Developed with ❤️ by Abril Montaño  
© 2023 Mexico Temperature Map
