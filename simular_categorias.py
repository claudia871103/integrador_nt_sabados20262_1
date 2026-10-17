import random
import uuid
import pandas as pd
from faker import Faker

#1. Establecer las constantes para los datos a simular
CATEGORIAS=[
    "Logística", "Tecnología", "Educación", "Medio ambiente", "Salud",
    "Emprendimiento", "Cultura", "Deporte", "Turismo", "Agricultura"
]
AREAS=["financiera", "mejora", "innovacion", "proyectos"]
FILAS=250
FALSITO = Faker("es_CO")

#2. Identificar los datos a simular con su tipo de dato
#id (texto (UUID)), nombre (texto), descripcion (texto).
#area_responsable (texto): columna EXTRA para el ejercicio de analisis;
#no pertenece al modelo de Backend II.

#3. Funcion generadora de los datos ordenados
def generar_datos(numero_filas=FILAS):
    categorias = []
    for _ in range(numero_filas):
        categorias.append({
            "id": str(uuid.uuid4()),
            "nombre": random.choice(CATEGORIAS),
            "descripcion": FALSITO.sentence(nb_words=8),
            "area_responsable": random.choice(AREAS)
        })
    return categorias

#4. Funcion para obtener una muestra de los datos
def obtener_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0,9999)).index

#5. Funcion auxiliar para cambiar la escritura del mismo nombre
def escribir_mal(texto):
    variantes=[texto.title(), texto.upper(), texto.lower(), f" {texto.lower()} "]
    return random.choice(variantes)

#6. Funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    #Nombre: variantes del mismo nombre, sin agregar categorias nuevas
    datos_df["nombre"]=datos_df["nombre"].map(escribir_mal)

    #Descripcion: 15% de los valores en None
    filas_elegidas=obtener_muestra(datos_df,0.15)
    datos_df.loc[filas_elegidas,"descripcion"]=None

    #Area responsable: 10% de los valores en None
    filas_elegidas=obtener_muestra(datos_df,0.10)
    datos_df.loc[filas_elegidas,"area_responsable"]=None

    #Duplicar el 8% de las filas completas, incluido el id.
    #Reemplazar filas completas conserva el total y los porcentajes de nulos.
    cantidad_duplicados=round(len(datos_df)*0.08)
    filas_completas=datos_df.dropna()
    if cantidad_duplicados:
        filas_elegidas=filas_completas.sample(
            n=cantidad_duplicados+1, random_state=random.randint(0,9999)
        ).index
        fila_original=datos_df.loc[filas_elegidas[0]].copy()
        for indice in filas_elegidas[1:]:
            datos_df.loc[indice]=fila_original

    return datos_df

#7. Generar y devolver el DataFrame para el script de exportacion
def generar_categorias(n=250):
    #Reiniciar las semillas permite reproducir los datos en cada llamada.
    #uuid.uuid4() usa aleatoriedad del sistema: los UUID cambian entre llamadas.
    Faker.seed(42)
    random.seed(42)
    df=pd.DataFrame(
        generar_datos(n), columns=["id", "nombre", "descripcion", "area_responsable"]
    )
    df=ensuciar(df)
    return df

#8. Revisar los datos sucios solo al ejecutar este archivo
if __name__ == "__main__":
    df=generar_categorias()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
