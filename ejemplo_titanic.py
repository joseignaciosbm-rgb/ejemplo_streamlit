import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# 1. Cargar el dataset
# Asumiendo que el archivo se llama 'database_titanic.csv' y se carga en un entorno como Streamlit/Jupyter
# Si estás en un entorno local, puedes usar: df = pd.read_csv('database_titanic.csv')
# Para este ejemplo, usaremos el nombre de archivo proporcionado:
try:
    df = pd.read_csv('database_titanic.csv')
except FileNotFoundError:
    print("Error: Asegúrate de que el archivo 'database_titanic.csv' esté en el directorio correcto.")
    # Crea un DataFrame de ejemplo si el archivo no se carga, solo para demostrar la lógica del gráfico
    data = {'PassengerId': [1, 2, 3, 4, 5],
            'Survived': [0, 1, 1, 1, 0],
            'Sex': ['male', 'female', 'female', 'female', 'male']}
    df = pd.DataFrame(data)

# 2. Agrupar los datos para el análisis
# Contamos cuántas personas sobrevivieron (1) o no (0) para cada sexo
survived_by_sex = df.groupby(['Sex', 'Survived']).size().unstack(fill_value=0)

# Renombrar las columnas para mayor claridad
survived_by_sex.columns = ['No Sobrevivió', 'Sobrevivió']

# 3. Crear el gráfico de barras
fig, ax = plt.subplots(figsize=(8, 6))

# Dibujar las barras
survived_by_sex.plot(kind='bar', ax=ax, rot=0)

# 4. Personalizar el gráfico
plt.title('Número de Sobrevivientes y No Sobrevivientes por Sexo')
plt.xlabel('Sexo')
plt.ylabel('Número de Personas')
plt.legend(title='Estado')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(ticks=[0, 1], labels=['Mujer', 'Hombre']) # Personalizar las etiquetas del eje X

# Mostrar los valores en las barras (opcional, pero útil)
for container in ax.containers:
    ax.bar_label(container, label_type='edge')

# Ajustar diseño
plt.tight_layout()

# 5. Mostrar el gráfico
plt.show()


