import streamlit as st
import time
import pandas as pd
from io import StringIO
from matplotlib import pyplot as plt
import plotly.express as px

# Le ponemos Nombre a la pagina
st.set_page_config(page_title='Prueba Tecnica Enki Trainee Data Scientist', layout='wide')

# Le ponemos el titulo de la prueba tecnica y el logo de enki

t1, t2 = st.columns((0.07, 1))

t1.image('images.png')
t2.title("Prueba Tecnica Enki para aspirante Trainee Data Scientist y Data Analyst")
t2.markdown("Esta web está pensada para que se puedan realizar las visualizaciones y procedimientos de la prueba técnica, debido a algunas dificultades que encontré para crear una cuenta de Power BI :(")

# Se exporta el conjunto de datos 

df_datosConsumo = pd.read_excel('Ejercicio_set_de_datos_PBI.xlsx', sheet_name='Datos_consumo')
df_catsect = pd.read_excel('Ejercicio_set_de_datos_PBI.xlsx', sheet_name='cat_sectores', header=0)
df_sociedades = pd.read_excel('Ejercicio_set_de_datos_PBI.xlsx', sheet_name='Sociedades', header=0)
df_tipoCliente = pd.read_excel('Ejercicio_set_de_datos_PBI.xlsx', sheet_name='Tipo de cliente')

st.header("Conjuntos de datos")
st.text("A Continuacion muestran los datafames junto con la informacion de cada uno. Esto va a ser importante, porque mas adelante de la prueba necesitaremos poner en el formato requerido los tipos de datos, y hacer uniones de tablas.")

# Primera Hoja
st.subheader("Primera Hoja Datos Consumo")
st.dataframe(df_datosConsumo.head(10))

# buffer para imprimir variables
buffer = StringIO()
df_datosConsumo.info(buf=buffer)
info_strDC = buffer.getvalue() # DC = Datos Consumo

# Imprimimos informacion
st.text(info_strDC)

# Segunda Hoja
st.subheader("Segunda Hoja Sociedades")
st.dataframe(df_sociedades.head(10))

# buffer para imprimir variables
buffer = StringIO()
df_sociedades.info(buf=buffer)
info_strS = buffer.getvalue() # S = Sociedades

# Imprimimos informacion
st.text(info_strS)

# Tercera Hoja
st.subheader("Tercera Hoja cat_sectores")
st.dataframe(df_catsect.head(10))

# buffer para imprimir variables
buffer = StringIO()
df_catsect.info(buf=buffer)
info_strCS = buffer.getvalue() # CS = Cat Sectores

# Imprimimos informacion
st.text(info_strCS)

# Cuarta Hoja
st.subheader("Tercera Hoja Tipo de Cliente")
st.dataframe(df_tipoCliente.head(10))

# buffer para imprimir variables
buffer = StringIO()
df_tipoCliente.info(buf=buffer)
info_strTC = buffer.getvalue() # TC = Tipo Cliente

# Imprimimos informacion
st.text(info_strTC)


# Explicacion del procedimiento 
st.subheader("Preprocesamiento de Datos")
st.text("A continuacion se realizan los procedimientos especificados en el documento de la prueba>")

# --- Preprocesamiento Primera Hoja: Datos Consumo

# Reemplazamos los espacios por guiones bajos
nuevos_nombres = []
for nombres_viejos in df_datosConsumo.columns:
    sin_espacios = nombres_viejos.replace(' ','_')
    nuevos_nombres.append(sin_espacios)
df_datosConsumo.columns = nuevos_nombres

# Renombramos las columnas que no se pueden hacer de forma automatica
df_datosConsumo.rename(columns={'Periodo_Fis': 'Periodo', 'codigo_sector': 'Codigo_sector'}, inplace=True)

# Convertimos a tipo String los datos de Tipo Object
df_datosConsumo[['Sociedad','Tipo_de_Cliente','Codigo_sector','Unidad','Segmento_Tarifario']] = df_datosConsumo[['Sociedad','Tipo_de_Cliente','Codigo_sector','Unidad','Segmento_Tarifario']].astype('string')

# Rellenamos valores nulos
df_datosConsumo[['Unidad','Segmento_Tarifario']] = df_datosConsumo[['Unidad','Segmento_Tarifario']].fillna('NA')
df_datosConsumo['Codigo_sector'] = df_datosConsumo['Codigo_sector'].fillna('NA')

# buffer para imprimir variables
buffer = StringIO()
df_datosConsumo.info(buf=buffer)
info_strDC = buffer.getvalue() # DC = Datos Consumo

# Imprimimos informacion ya preprocesada
st.markdown("**La informacion de la tabla de Datos Consumo Procesada: **")
st.text(info_strDC)

# ---- Preprocesamiento Segunda Hoja: Sociedades

df_sociedades.rename(columns={'Sociedad clave': 'Sociedad'}, inplace=True)

# buffer para imprimir variables
buffer = StringIO()
df_sociedades.info(buf=buffer)
info_strS = buffer.getvalue() # S = Sociedades

# Imprimimos informacion
st.markdown("**Informacion de la tabla de Sociedades Procesada: **")
st.text("En esta, mas adelante se va a necesitar realizar un merge, por lo que para que los nombre de las columnas coincidan se realizo el cambio")
st.text(info_strS)


# --- Preprocesamiento Tercera Hoja: Cat Sectores

df_catsect.rename(columns={'codigo de sector':'Codigo_sector'}, inplace=True)

# buffer para imprimir variables
buffer = StringIO()
df_catsect.info(buf=buffer)
info_strCS = buffer.getvalue() # CS = Cat Sectores

# Imprimimos informacion
st.markdown("**Informacion de la tabla de Cat Sectores Procesada: **")
st.text("En esta, mas adelante se va a necesitar realizar un merge, por lo que para que los nombre de las columnas coincidan se realizo el cambio")
st.text(info_strCS)

# --- Preprocesamiento Cuarta Hoja: Tipo de Cliente 

df_tipoCliente.rename(columns={'Clave cliente':'Tipo_de_Cliente'}, inplace=True)

# buffer para imprimir variables
buffer = StringIO()
df_tipoCliente.info(buf=buffer)
info_strTC = buffer.getvalue() # TC = Tipo Cliente

# Imprimimos informacion
st.markdown("**Informacion de la tabla Tipo Cliente Procesada: **")
st.text("En esta, mas adelante se va a necesitar realizar un merge, por lo que para que los nombre de las columnas coincidan se realizo el cambio")
st.text(info_strTC)

    # ---- Relaciones entre tablas ------ #

st.header("Uniones de Tablas")
st.subheader("Realizamos la union de las tablas para su analisis con graficos")

# Primera Union
Sociedades_datosConsumo_merge = pd.merge(df_datosConsumo, df_sociedades, on='Sociedad', how='left')

st.text("Primera Union Datos Consumo - Sociedades")
st.text("SE muestran las primeras 10 filas")

st.dataframe(Sociedades_datosConsumo_merge.head(10))

# Segunda Union
df_unido = pd.merge(Sociedades_datosConsumo_merge, df_catsect, on='Codigo_sector', how='left')

st.text("Realizamos la segunda union de Tablas Consumo - Cat Sectores")
st.text("SE muestran las primeras 10 filas")

st.dataframe(df_unido.head(10))

    # --- Medidas y Columnas --- #

st.header("Medidas y Columnas")
st.subheader("Creamos las columnas que nos piden para calcuar el IVA y el Total")

# Calculo del IVA
df_unido['IVA'] = df_unido['Consumo_Mes'] * 0.16

# buffer para imprimir variables
buffer = StringIO()
df_unido['IVA'].info(buf=buffer)
info_strIVA = buffer.getvalue() # U = Unido

# Imprimimos informacion
st.text(info_strIVA)

# Calculo del Total

df_unido['Total'] = df_unido['Consumo_Mes'] + df_unido['IVA']

# buffer para imprimir variables
buffer = StringIO()
df_unido['Total'].info(buf=buffer)
info_strT = buffer.getvalue() # T = Total

# Imprimimos informacion
st.text(info_strT)

# Ultima Union para Tipo De Cliente

st.text("Realizamos una ultima union para incluir el tipo de cliente en nuestro analisis")

df_final = pd.merge(df_unido, df_tipoCliente, on='Tipo_de_Cliente', how='left')

# Formato de las columnas
lista_columnas = ['Sociedad','Tipo_de_Cliente','Codigo_sector','Sociedad descripcion','Descripcion sector / giro','Descripcion']

df_final[lista_columnas] = df_final[lista_columnas].astype('string')

st.dataframe(df_final.head(10))

# buffer para imprimir variables
buffer = StringIO()
df_final.info(buf=buffer)
info_strFinal = buffer.getvalue() # T = Total

# Imprimimos informacion
st.text(info_strFinal)

    # --- Graficos --- #

# Grafica de Barras
df_barras = df_final.groupby('Descripcion')['Total'].sum().reset_index()

# Crear el gráfico de barras
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df_barras['Descripcion'], df_barras['Total'])

# Configurar títulos y etiquetas
ax.set_title('Total por Descripción', fontsize=16)
ax.set_xlabel('Descripción', fontsize=12)
ax.set_ylabel('Total', fontsize=12)

# Rotar las etiquetas del eje X si son muy largas
plt.xticks(rotation=90, ha='right')

# Ajustar el espaciado
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.header("Grafico de Barras")
st.pyplot(fig)


# Grafico de Pie
df_pie = df_final.groupby('Tipo_de_Cliente')['Total'].sum().reset_index()

# Crear el gráfico de pie
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df_pie['Total'], labels=df_pie['Tipo_de_Cliente'], autopct='%1.1f%%', startangle=140)

# Configurar título
ax.set_title('Distribución de Total por Tipo de Cliente', fontsize=16)

# Mostrar el gráfico en Streamlit
st.header("Grafico de Pie")
plt.axis('equal')  # Para que el pie se vea como un círculo
st.pyplot(fig)

