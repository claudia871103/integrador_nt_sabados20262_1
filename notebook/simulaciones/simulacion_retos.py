"""
Script para simular 500 filas de la tabla retos usando Faker,
y despues ensuciar los datos a proposito para practicar limpieza de datos.
"""

import random
import uuid
from datetime import timedelta

import pandas as pd
from faker import Faker

# Faker en español de Colombia
fake = Faker("es_CO")

# Semillas fijas para que el resultado sea siempre el mismo
Faker.seed(42)
random.seed(42)

# --- Constantes ---
ESTADOS = ["pendiente", "en_curso", "cerrado", "cancelado"]
IDS_EMPRESA = [str(uuid.uuid4()) for _ in range(10)]
IDS_CATEGORIA = [str(uuid.uuid4()) for _ in range(6)]
IDS_PRIORIDAD = [str(uuid.uuid4()) for _ in range(3)]


def generar_retos(n=500):
    filas = []

    # 1) Generar las filas "limpias" con Faker
    for _ in range(n):
        fecha_inicio = fake.date_between(start_date="-1y", end_date="+3m")
        fecha_fin = fecha_inicio + timedelta(days=random.randint(15, 180))

        fila = {
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=6).rstrip("."),
            "descripcion": fake.sentence(nb_words=12),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "estado": random.choice(ESTADOS),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categoria": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD),
        }
        filas.append(fila)

    df = pd.DataFrame(filas)
    total = len(df)

    # 2) Ensuciar "nombre": 10% con espacios sobrantes
    cantidad = int(total * 0.10)
    indices = random.sample(range(total), cantidad)
    for i in indices:
        df.loc[i, "nombre"] = "   " + df.loc[i, "nombre"] + "   "

    # 3) Ensuciar "descripcion": 12% en None (nulos)
    cantidad = int(total * 0.12)
    indices = random.sample(range(total), cantidad)
    for i in indices:
        df.loc[i, "descripcion"] = None

    # 4) Ensuciar "fecha_fin": 8% en None y 5% anterior a fecha_inicio
    # (se hace antes de convertir fecha_inicio a texto, porque aqui se
    # necesita todavia como fecha para poder restarle dias)
    indices_disponibles = list(range(total))
    random.shuffle(indices_disponibles)

    cantidad_nulos = int(total * 0.08)
    cantidad_anteriores = int(total * 0.05)

    indices_nulos = indices_disponibles[:cantidad_nulos]
    indices_anteriores = indices_disponibles[cantidad_nulos:cantidad_nulos + cantidad_anteriores]

    for i in indices_nulos:
        df.loc[i, "fecha_fin"] = None

    for i in indices_anteriores:
        # error logico a proposito: fecha_fin queda ANTES que fecha_inicio
        df.loc[i, "fecha_fin"] = df.loc[i, "fecha_inicio"] - timedelta(days=random.randint(1, 60))

    # 5) Ensuciar "fecha_inicio": mezclar dos formatos de texto
    fechas_nuevas = []
    for valor in df["fecha_inicio"]:
        if random.random() < 0.5:
            fechas_nuevas.append(valor.strftime("%Y-%m-%d"))  # ej: 2026-03-02
        else:
            fechas_nuevas.append(valor.strftime("%d/%m/%Y"))  # ej: 02/03/2026
    df["fecha_inicio"] = fechas_nuevas

    # 6) Ensuciar "estado": variantes de mayusculas y espacios
    variantes = {
        "en_curso": ["en_curso", "EN CURSO"],
        "cerrado": ["cerrado", " Cerrado "],
    }
    for i in range(total):
        estado_actual = df.loc[i, "estado"]
        if estado_actual in variantes and random.random() < 0.5:
            df.loc[i, "estado"] = random.choice(variantes[estado_actual])

    # 7) Duplicar 5% de las filas tal cual (duplicados exactos)
    cantidad_duplicados = int(total * 0.05)
    filas_duplicadas = df.sample(n=cantidad_duplicados, random_state=42)
    df = pd.concat([df, filas_duplicadas], ignore_index=True)

    return df


if _name_ == "_main_":
    df = generar_retos(FILAS)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())