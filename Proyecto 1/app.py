import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Dashboard de Vehículos", layout="wide")

# Título principal
st.title("🚗 Dashboard de Análisis de Vehículos en Venta")
st.markdown("Explora datos de anuncios de vehículos mediante visualizaciones interactivas.")

# Carga de datos
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_us.csv')
    return df

car_data = load_data()

# Sidebar con controles
st.sidebar.header("⚙️ Controles de Visualización")

# Mostrar datos crudos (opcional)
if st.sidebar.checkbox("Mostrar datos crudos"):
    st.subheader("📄 Vista previa de los datos")
    st.dataframe(car_data.head())

# Selección de columnas para gráficos
numeric_cols = car_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_cols = car_data.select_dtypes(include=['object']).columns.tolist()

# Histograma
st.header("📊 Histograma")
hist_col = st.selectbox("Selecciona columna para histograma:", numeric_cols, index=numeric_cols.index("odometer") if "odometer" in numeric_cols else 0)
if st.button("Generar histograma"):
    fig = px.histogram(car_data, x=hist_col, title=f"Distribución de {hist_col}", nbins=50)
    fig.update_layout(xaxis_title=hist_col, yaxis_title="Frecuencia")
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersión
st.header("📈 Gráfico de Dispersión")
col_x = st.selectbox("Eje X:", numeric_cols, index=numeric_cols.index("odometer") if "odometer" in numeric_cols else 0)
col_y = st.selectbox("Eje Y:", numeric_cols, index=numeric_cols.index("price") if "price" in numeric_cols else 1)
if st.button("Generar gráfico de dispersión"):
    fig = px.scatter(car_data, x=col_x, y=col_y, title=f"{col_y} vs {col_x}", opacity=0.6)
    fig.update_layout(xaxis_title=col_x, yaxis_title=col_y)
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de barras por condición
st.header("📌 Vehículos por Condición")
if st.checkbox("Mostrar gráfico de barras por condición"):
    condition_counts = car_data['condition'].value_counts().reset_index()
    condition_counts.columns = ['condition', 'count']
    fig = px.bar(condition_counts, x='condition', y='count', title="Cantidad de vehículos por condición", color='condition')
    st.plotly_chart(fig, use_container_width=True)

# Filtro interactivo
st.sidebar.header("🔍 Filtrar datos")
price_range = st.sidebar.slider(
    "Rango de precio:",
    min_value=int(car_data['price'].min()),
    max_value=int(car_data['price'].max()),
    value=(int(car_data['price'].min()), int(car_data['price'].max()))
)

filtered_data = car_data[(car_data['price'] >= price_range[0]) & (car_data['price'] <= price_range[1])]
st.sidebar.write(f"📊 Vehículos filtrados: {len(filtered_data)} de {len(car_data)}")

# Estadísticas básicas
st.sidebar.header("📈 Estadísticas")
if st.sidebar.checkbox("Mostrar estadísticas descriptivas"):
    st.sidebar.write(filtered_data['price'].describe())

# Pie de página
st.markdown("---")
st.markdown("**Dashboard creado con Streamlit, Plotly Express y Pandas** | Datos: vehicles_us.csv")