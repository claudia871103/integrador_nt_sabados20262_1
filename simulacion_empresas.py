'''
Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`. Con la libreria **Faker** genera 300 filas falsas de la tabla `empresas`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.
Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tAu compañero pueda reproducirlo. '''

import random
import uuid
import pandas as pd
from faker import Faker


#1. Sembrar semillas para los datos a simular 
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con tu tipo de dato
# id (texto (UUID)), 
# nombre (texto), 
# nit (texto), 
# sector (texto) ********************,
# contacto (texto), 
# correo (texto), 
# telefono (texto), 
# activa (booleano).

#3. Establecer una constante para el numero de simulaciones 
FILAS=400
SECTORES=["comercio","industrial","educacion","financiero"]
FALSITO=Faker("es_CO")

#4. Funcion generadora
def generar_datos(numero_filas=400):
    empresas=[]
    for _ in range(numero_filas):
        empresas.append({
            "id":str(uuid.uuid4),
            "nombre":FALSITO.name(),
            "nit":FALSITO.numerify(),
            "sector":random.choice(SECTORES),
            "contacto":FALSITO.name(),            
            "correo":FALSITO.email(),            
            "telefono":FALSITO.numerify(),
            "activa":random.choice([True,False]),           
        })
    return empresas

#5. conviertiendo los datos generados en dataframe con PANDAS
        
tabla_ordenada_empresas=pd.DataFrame(generar_datos())

#6. probar la funcion
print(tabla_ordenada_empresas)

#7. Preparar la simulacion para ensuciar mis datos

#7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos,porcentaje):
    return datos.sample(fraccion=porcentaje,random_state=random.randint(0,9999)).index

#7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal():
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f" {texto} ","Juan Jose"]
    return random.choice(variantes)

#7.3 Funcion Auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI","1"])    
    else:
        return random.choice(["NO","0"])

#7.4 Funcion para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    #Nombre: el 10% tenga espacios y el 15% este en mayuscula
    filas_elegidas=obtener_muestra(datos_df,0.1)
    datos_df.loc[filas_elegidas,"nombre"]=" "+datos_df.loc[filas_elegidas,"nombre"]+""

    filas_elegidas=obtener_muestra(datos_df,0.15)
    datos_df.loc[filas_elegidas,"nombre"]=datos_df.loc[filas_elegidas,"nombre"].str.upper()

    



