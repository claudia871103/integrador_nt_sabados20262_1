'''
Clasifica tematicamente los retos. Crea el script src/simular_categorias.py. Con la libreria *Faker* genera 250 filas falsas de la tabla categorias, con las MISMAS columnas que usa Backend II. Despues *ensucia los datos a proposito*: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.
Usa Faker("es_CO") y fija la semilla con Faker.seed(42) y random.seed(42) para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.
OJO: area_responsable NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar. Dejala anotada como tal en el script.'''

import random 
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. IdentiFicar los datos a simular con su tipo de dato
#id (texto (UUID)), 
#nombre (texto), 
#descripcion (texto), 
#area_responsable (texto): columna extra para el ejercicio de analisis.

#3. ESTABLECER UNA CONSTANTE PARA EL NUEMROD E SIMULACIONS
FILAS=250
CATEGORIAS=["tecnologia", "educacion", "medio ambiente", "salud", "emprendimiento"]
AREAS=["financiera", "mejora", "innovacion", "proyectos" ]
FALSITO = Faker("es_CO")

#4. Funcion generadora
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

#5. Convirtiendo los datos generados en un dataframe con PANDAS
tabla_ordenada_categorias=pd.DataFrame(generar_datos())

#6. Probar la funcion
print(tabla_ordenada_categorias)

#7. Preparar la simulacion para ensuciar mis datos

#7.1 Funcion para obtener una muestra de los datos 
def obtener_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0,9999)).index


#7.2 Funciona auxiliar para cambiar valores de un texto 
def escribir_mal (texto):
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f"{texto} ",f" {texto}",f" {texto} ", "Juan Jose"]
    return random.choice(variantes)

#7.3 Funcion auxiliar para cambiar los booleanos 
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI","1"])  
    else:
        return random.choice(["NO","0"])

    #7.4 Funcion para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df=datos_df.copy()

#Nombre: el 10% tenga espacios y el 8% este en mayuscula
    filas_elegidas=obtener_muestra(datos_df,0.1)
    datos_df.loc[filas_elegidas,"nombre"]=" "+datos_df.loc[filas_elegidas,"nombre"]+""

    filas_elegidas=obtener_muestra(datos_df,0.08)
    datos_df.loc[filas_elegidas,"nombre"]=datos_df.loc[filas_elegidas,"nombre"].str.upper()

#correo: el 5% de los datos este sin @
    filas_elegidas=obtener_muestra(datos_df,0.05)
    datos_df.log[filas_elegidas,"correo"]=datos_df.log[filas_elegidas,"correo"].str.replace("@","")

#El 4% de los correos no deberia tener ningun valor (None)
    filas_elegidas=obtener_muestra(datos_df,0.04)
    datos_df.loc[filas_elegidas,"correo"]=None    

#Rol: Aplicar errores de escritura (variantes)
    filas_elegidas=obtener_muestra(datos_df,0.1)  
    datos_df.loc[filas_elegidas,"rol"]=datos_df.loc[filas_elegidas,"rol"].map(escribir_mal)

#Activo: En ocasiones llega SI, NO, 1, 0.
    datos_df["activo"]=datos_df["activo"].astype(object)
    filas_elegidas=obtener_muestra(datos_df,0.15)
    datos_df.loc[filas_elegidas,"activo"]=datos_df.loc[filas_elegidas,"activo"].map(convertir_booleano)

#Mezclar el formato de la fecha
#ISO => 2026-10-03 YYYY-mm-dd HH:MM:SS
#LATINO => d/m/y h:m
    iso=datos_df["fecha_registro"].dt.strtime("%Y-%m-%d %H:%M:%S")
    latino=datos_df["fecha_registro"].dt.strtime("%d/%m/%y %H:%m")
    datos_df["fecha_registro"]=iso
    filas_elegidas=obtener_muestra(datos_df,0.25)
    datos_df.loc[filas_elegidas,"fecha_registro"]=latino.loc[filas_elegidas]
    



