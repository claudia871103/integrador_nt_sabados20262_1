'''
Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`.
Con la libreria Faker genera 300 filas falsas de la tabla empresas.
Despues ensucia los datos a proposito para practicar limpieza.
'''

import random
import uuid
import pandas as pd
from faker import Faker


#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con tu tipo de dato
# id (texto UUID)
# nombre (texto)
# nit (texto)
# sector (texto)
# contacto (texto)
# correo (texto)
# telefono (texto)
# activa (booleano)

#3. Establecer una constante para el numero de simulaciones
FILAS = 300
SECTORES = ["comercio", "industrial", "educacion", "financiero"]
FALSITO = Faker("es_CO")


#4. Funcion generadora
def generar_datos(numero_filas=FILAS):
    empresas = []

    for _ in range(numero_filas):
        empresas.append({
            "id": str(uuid.uuid4()),
            "nombre": FALSITO.company(),
            "nit": FALSITO.numerify("#########-#"),
            "sector": random.choice(SECTORES),
            "contacto": FALSITO.name(),
            "correo": FALSITO.company_email(),
            "telefono": FALSITO.numerify("3#########"),
            "activa": random.choice([True, False])
        })

    return empresas


#5. Funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 9999)
    ).index


#6. Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes = [
        texto.title(),
        texto.upper(),
        f" {texto.lower()} "
    ]

    return random.choice(variantes)


#7. Funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else:
        return random.choice(["No", "0"])


def poner_puntos_nit(nit):
    nit = nit.replace("-", "")

    return nit[:3] + "." + nit[3:6] + "." + nit[6:9] + "-" + nit[9]


def telefono_con_espacios(telefono):
    return telefono[:3] + " " + telefono[3:6] + " " + telefono[6:]


def telefono_internacional(telefono):
    return "+57 " + telefono[:3] + "-" + telefono[3:6] + "-" + telefono[6:]


#7.4 Funcion para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # Nombre: 10% con espacios y 15% en mayuscula
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"] = (
        " " + datos_df.loc[filas_elegidas, "nombre"] + " "
    )

    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[
        filas_elegidas, "nombre"
    ].str.upper()

    # NIT: mitad con puntos y guion, mitad sin formato
    filas_elegidas = obtener_muestra(datos_df, 0.50)

    datos_df.loc[filas_elegidas, "nit"] = datos_df.loc[
        filas_elegidas, "nit"
    ].map(poner_puntos_nit)

    filas_sin_formato = datos_df.index.difference(filas_elegidas)

    datos_df.loc[filas_sin_formato, "nit"] = datos_df.loc[
        filas_sin_formato, "nit"
    ].str.replace("-", "", regex=False)

    # Sector: variantes en mayusculas y espacios
    filas_elegidas = obtener_muestra(datos_df, 0.10)

    datos_df.loc[filas_elegidas, "sector"] = datos_df.loc[
        filas_elegidas, "sector"
    ].map(escribir_mal)

    # Contacto: 8% con dato nulo
    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "contacto"] = None

    # Correo: 6% sin arroba
    filas_elegidas = obtener_muestra(datos_df, 0.06)

    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[
        filas_elegidas, "correo"
    ].str.replace("@", "", regex=False)

    # Telefono: tres formatos diferentes
    filas_con_espacios = obtener_muestra(datos_df, 0.33)

    datos_df.loc[filas_con_espacios, "telefono"] = datos_df.loc[
        filas_con_espacios, "telefono"
    ].map(telefono_con_espacios)

    filas_restantes = datos_df.index.difference(filas_con_espacios)

    filas_internacionales = datos_df.loc[filas_restantes].sample(
        frac=0.50,
        random_state=random.randint(0, 9999)
    ).index

    datos_df.loc[filas_internacionales, "telefono"] = datos_df.loc[
        filas_internacionales, "telefono"
    ].map(telefono_internacional)

    # Activa: algunos valores quedan como texto
    datos_df["activa"] = datos_df["activa"].astype(object)

    filas_elegidas = obtener_muestra(datos_df, 0.15)

    datos_df.loc[filas_elegidas, "activa"] = datos_df.loc[
        filas_elegidas, "activa"
    ].map(convertir_booleano)

    # 3% de NIT repetidos entre empresas diferentes
    filas_nit_repetidos = obtener_muestra(datos_df, 0.03)

    nits_para_repetir = datos_df.loc[
        datos_df.index.difference(filas_nit_repetidos), "nit"
    ].sample(
        n=len(filas_nit_repetidos),
        random_state=42
    ).values

    datos_df.loc[filas_nit_repetidos, "nit"] = nits_para_repetir

    # 5% de filas duplicadas exactamente iguales
    cantidad_duplicados = int(len(datos_df) * 0.05)

    duplicados = datos_df.sample(
        n=cantidad_duplicados,
        random_state=42
    )

    datos_df = pd.concat(
        [datos_df, duplicados],
        ignore_index=True
    )

    return datos_df


#8. Funcion principal que genera y devuelve el DataFrame
def generar_empresas(n=FILAS):
    tabla_ordenada_empresas = pd.DataFrame(generar_datos(n))

    tabla_sucia_empresas = ensuciar(tabla_ordenada_empresas)

    return tabla_sucia_empresas


#9. Probar la funcion solo cuando se ejecute este archivo
if __name__ == "__main__":
    df = generar_empresas()

    print(df.shape)
    print(df.head())
    print(df.isna().sum())