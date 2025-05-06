import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Lectura de datos

df = pd.read_csv("../../../data/final/datos_finales.csv", sep = ';')

#Configuración de la página

st.set_page_config(
    page_title = 'Herramienta de VIsualización de Datos -13MBID',
    page_icon = '📊',
    layout = 'wide',
)

#Título de la aplicación
st.title('Herramienta de Visualización de Datos - 13MBID')
st.write('Esta aplicación permite explorar y visualizar los datos del proyecto en curso.')
st.write('Desarrollado por: Verónica Puerto Belda')
st.markdown('----')

#Gráficos
st.header('Gráficos')
st.subheader('Caracterización de los créditos otorgados')

# Cantidad de créditos por objetivo del mismo
#st.write('Distribución de créditos según su objetivo:')
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

#Visualización 
st.plotly_chart(creditos_x_objetivo, use_container_width=True)

# Histograma de los importes de créditos otorgados
#st.write('Distribución de importes de los créditos solicitados:')
histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')
st.plotly_chart(histograma_importes, use_container_width=True)

# Conteo de ocurrencias por estado
estado_credito_counts = df['estado_credito_N'].value_counts()

# Gráfico de torta de estos valores
fig1 = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
fig1.update_layout(title_text='Distribución de créditos por estado registrado')
st.plotly_chart(fig1, use_container_width=True)

falta_pago_counts = df['falta_pago'].value_counts()

# Create a Pie chart
fig2 = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
fig2.update_layout(title_text='Distribución de créditos en función de registro de mora')
st.plotly_chart(fig2, use_container_width=True)

# Definir el orden personalizado
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']

# Ordenar los datos según el orden personalizado
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

# Crear el gráfico de líneas
lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')
st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)


# Gráfico de barras apiladas: Comparar la distribución de créditos por estado y objetivo
barras_apiladas = px.histogram(df, x='objetivo_credito', color='estado_credito_N', 
                               title='Distribución de créditos por estado y objetivo',
                               barmode='stack')
barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')
st.plotly_chart(barras_apiladas, use_container_width=True)

# 1. Distribución de los importes solicitados por objetivo del crédito (gráfico de cajas)
grafico_cajas = px.box(df, 
                      x='objetivo_credito', 
                      y='importe_solicitado',
                      title='Distribución de importes solicitados por objetivo del crédito',
                      color='objetivo_credito')

grafico_cajas.update_layout(
    xaxis_title='Objetivo del crédito',
    yaxis_title='Importe solicitado',
    showlegend=False  # Opcional: ocultar leyenda ya que el color es redundante con el eje x
)

st.plotly_chart(grafico_cajas, use_container_width=True)

#Se agrega un selector para el tipo de crédito y se aplica en los gráficos siguentes:
tipo_credito = st.selectbox(
    "Selecciona el tipo de crédito",
    df['objetivo_credito'].unique(),
)

st.write('Tipo de crédito seleccionado:', tipo_credito)
#Filtrar el DataFrame según el tipo de credito seleccionado
df_filtrado = df[df['objetivo_credito'] == tipo_credito]

col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras apiladas: Comparar la distribución de créditos por estado y objetivo
    barras_apiladas = px.histogram(df_filtrado, x='objetivo_credito', color='estado_credito_N', 
                                title='Distribución de créditos por estado y objetivo',
                                barmode='stack')
    barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')
    st.plotly_chart(barras_apiladas, use_container_width=True)

with col2:
    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    # Create a Pie chart
    fig_mora_filtrada = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig_mora_filtrada.update_layout(title_text='Distribución de créditos en función de registro de mora')
    st.plotly_chart(fig_mora_filtrada, use_container_width=True)