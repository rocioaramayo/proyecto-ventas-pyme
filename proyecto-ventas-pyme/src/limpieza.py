from pathlib import Path

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
CARPETA_RAW = RAIZ / "data" / "raw"
CARPETA_PROCESSED = RAIZ / "data" / "processed"
CARPETA_PROCESSED.mkdir(parents=True, exist_ok=True)

# 1. Cargar archivos
ventas = pd.read_csv(CARPETA_RAW / "ventas.csv")
productos = pd.read_csv(CARPETA_RAW / "productos.csv")
clientes = pd.read_csv(CARPETA_RAW / "clientes.csv")
sucursales = pd.read_csv(CARPETA_RAW / "sucursales.csv")

# 2. Explorar los datos
print("Primeras filas:")
print(ventas.head())

print("\nInformación general:")
ventas.info()

print("\nValores nulos:")
print(ventas.isna().sum())

print("\nDuplicados:")
print(ventas.duplicated().sum())

print("\nDescripción de cantidad:")
print(ventas["cantidad"].describe())

print("\nDescripción de precios:")
print(ventas["precio_unitario"].describe())

print("\nDescripción de descuentos:")
print(ventas["descuento"].describe())

# 3. Limpiar
ventas = ventas.drop_duplicates()

ventas["fecha"] = pd.to_datetime(
    ventas["fecha"],
    errors="coerce"
)

ventas["cantidad"] = pd.to_numeric(
    ventas["cantidad"],
    errors="coerce"
)

ventas["precio_unitario"] = pd.to_numeric(
    ventas["precio_unitario"],
    errors="coerce"
)

ventas["descuento"] = pd.to_numeric(
    ventas["descuento"],
    errors="coerce"
)

ventas = ventas[
    (ventas["cantidad"] > 0)
    & (ventas["precio_unitario"] > 0)
    & (ventas["descuento"].between(0, 1))
    & (ventas["fecha"].notna())
]

# 4. Guardar resultado
ventas.to_csv(
    CARPETA_PROCESSED / "ventas_limpias.csv",
    index=False
)

print("\nLimpieza terminada.")
print(f"Filas finales: {len(ventas)}")
print("Archivo creado: data/processed/ventas_limpias.csv")
