'''
Simular 800 filas de registros con Faker y ensuciarlas a proposito


Tabla puente: vincula un Usuario con un Reto y deja trazabilidad. 
Crea el script src/simular_registros.py. 
Con la libreria *Faker* genera 800 filas falsas de la tabla registros, 
con las MISMAS columnas que usa Backend II. Despues 
*ensucia los datos a proposito*: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos.
 Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa Faker("es_CO") y fija la semilla con Faker.seed(42) y random.seed(42) 
para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.
'''
import random
import uuid
 
import pandas as pd
from faker import Faker
 
fake = Faker("es_CO")
 
Faker.seed(42)
random.seed(42)

#3. identifica los datos que dedo simular 

# id (texto (UUID)), fecha_registro (fecha y hora), observacion (texto), 
# estado (texto), id_usuario (texto (UUID)), id_reto (texto (UUID)).

#id
#fecha_registro
#hora_registro
#observación
#estado
#id_usuario
#id_reto


#4. identifico los datos o el dato que sea de salector 
ESTADOS = ["inscrito", "en proceso", "finalizado"]

N_USUARIOS = 150
N_RETOS = 40
IDS_USUARIO = [str(uuid.uuid4()) for _ in range(N_USUARIOS)]
IDS_RETO = [str(uuid.uuid4()) for _ in range(N_RETOS)]
 

#5. defino mi DATASET 
FILAS=800

#6. contruyo una funcion para generar los N datos pedidos (LIMPIOS)
def _generar_datos_limpios(n):
    """Genera n filas limpias como lista de diccionarios."""
    filas = []
    for _ in range(n):
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })
    return filas


#ensuciar los datos

#1. crear una función para definir porcentajes de error (procesos stockasticos, inyectar un porcentaje de error para controlar que no se ensucien todos)
#esta función si la puedo copiar y pegar tal ceul en mi proyecto
def _generar_muestra(datos,porcentaje):
  return datos.sample(frac=porcentaje,random_state=random.randint(0,999)).index

#2. crear una función para escribir mal un texto
def _escribir_mal(texto):
  variantes=[texto.lower(), f" {texto.title()} ", texto.capitalize(), texto.upper()]
  return random.choice(variantes)

#3. función para convertir boooleanos en textos
def _convertir_booleano_texto(valor):
  if valor:
    return random.choice(["SI", "1"])
  return random.choice(["NO", "0"])

  #4. Función para ensuciar los datos
def _ensuciar(datos_df):
  datos_df=datos_df.copy()

  #DATOS SUCIOS SOLICITADOS POR EL EJERCICIO

  #Se ensucia fecha_registro: dos formatos mezclados: "2026-03-15 14:30:00" y "15/03/2026 14:30".
  iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
  latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
  datos_df["fecha_registro"] = iso
  filas_elegidas = _generar_muestra(datos_df, 0.10)
  datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas]

  #Se ensucia observacion: 20% en None (nulos).
  filas_elegidas = _generar_muestra(datos_df,0.20) 
  datos_df.loc[filas_elegidas,"observacion"]=None

  #Se ensucia estado: variantes: 'inscrito', 'EN PROCESO', ' Finalizado '. usar el ejemplo de escribir mal
  filas_elegidas = _generar_muestra(datos_df, 0.07)
  datos_df.loc[filas_elegidas, "estado"] = (datos_df.loc[filas_elegidas, "estado"].map(_escribir_mal))

  #10% con el par id_usuario + id_reto REPETIDO: el mismo usuario inscrito dos veces en el mismo reto (eso el back lo prohibe con 409).
  cantidad = max(1, int(len(datos_df) * 0.10))
  duplicados_pareja = datos_df.sample(n=cantidad, random_state=42).copy()
  duplicados_pareja["id"] = [str(uuid.uuid4()) for _ in range(len(duplicados_pareja))]
  datos_df = pd.concat([datos_df, duplicados_pareja], ignore_index=True)

  #5% de las filas repetidas tal cual (duplicados exactos).
  filas_elegidas = _generar_muestra(datos_df, 0.05)
  duplicados_exactos = datos_df.loc[filas_elegidas]
  datos_df = pd.concat([datos_df, duplicados_exactos], ignore_index=True)

  return datos_df
 
def generar_registros(n=FILAS):
    df = pd.DataFrame(_generar_datos_limpios(n))
    df = _ensuciar(df)
    return df
 
 
if _name_ == "_main_":
    df = generar_registros(FILAS)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())