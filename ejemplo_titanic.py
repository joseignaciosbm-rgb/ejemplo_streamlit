import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Carga el archivo CSV "database_titanic.csv" en un DataFrame de pandas.
df = pd.read_csv("database_titanic.csv")

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

# Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
with st.sidebar:
    # Título para la sección de opciones en la barra lateral.
    st.write("# Opciones")
    
    # Crea un control deslizante (slider) que permite al usuario seleccionar un número de bins
    # en el rango de 0 a 10, con un valor predeterminado de 2.
    div = st.slider('Número de bins:', 0, 10, 2)
    
    # Muestra el valor actual del slider en la barra lateral.
    st.write("Bins=", div)

# Desplegamos un histograma con los datos del eje X
fig, ax = plt.subplots(1, 2, figsize=(10, 3))
ax[0].hist(df["Age"], bins=div)
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Histograma de edades")

# Tomando datos para hombres y contando la cantidad
df_male = df[df["Sex"] == "male"]
cant_male = len(df_male)

# Tomando datos para mujeres y contando la cantidad
df_female = df[df["Sex"] == "female"]
cant_female = len(df_female)

ax[1].bar(["Masculino", "Femenino"], [cant_male, cant_female], color = "red")
ax[1].set_xlabel("Sexo")
ax[1].set_ylabel("Cantidad")
ax[1].set_title('Distribución de hombres y mujeres')

# Desplegamos el gráfico
st.pyplot(fig)

st.write("""
## Muestra de datos cargados
""")
# Graficamos una tabla
st.table(df.head())

st.set_page_config(layout="wide")
st.title("🚢 Análisis de Supervivencia del Titanic: Sexo")
st.markdown("Visualización del número de sobrevivientes y no sobrevivientes agrupados por sexo.")


# --- 2. Cargar el Dataset ---
@st.cache_data # Recomendado para mejorar el rendimiento
def load_data(file_name):
   
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        st.error(f"Error: No se encontró el archivo '{file_name}'. Asegúrate de que esté en el mismo directorio.")
        return pd.DataFrame() # Retorna un DataFrame vacío en caso de error

    return df

df = load_data('database_titanic.csv')

if not df.empty:
    # --- 3. Procesar y Agrupar los Datos ---
    # Contamos cuántas personas sobrevivieron (1) o no (0) para cada sexo
    survived_by_sex = df.groupby(['Sex', 'Survived']).size().unstack(fill_value=0)

    # Renombrar las columnas para mayor claridad
    survived_by_sex.columns = ['No Sobrevivió', 'Sobrevivió']

    # Mostrar la tabla de datos
    st.subheader("Tabla de Datos Agrupados")
    st.dataframe(survived_by_sex)


    # --- 4. Crear la Figura de Matplotlib ---
    fig, ax = plt.subplots(figsize=(8, 6))

    # Dibujar las barras usando los ejes 'ax'
    survived_by_sex.plot(kind='bar', ax=ax, rot=0)

    # Personalizar el gráfico
    ax.set_title('Número de Sobrevivientes y No Sobrevivientes por Sexo')
    ax.set_xlabel('Sexo')
    ax.set_ylabel('Número de Personas')
    ax.legend(title='Estado')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_xticks(ticks=[0, 1], labels=['Mujer', 'Hombre']) # Personalizar las etiquetas del eje X

    # Mostrar los valores en las barras (opcional)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge')

    plt.tight_layout()


    # --- 5. Mostrar la Figura en Streamlit (¡Solución!) ---
    # Streamlit necesita que se le pase el objeto figura (fig)
    st.subheader("Gráfico de Barras")
    st.pyplot(fig)
