from pathlib import Path

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
CARPETA_RAW = RAIZ / "data" / "raw"
CARPETA_PROCESSED = RAIZ / "data" / "processed"
CARPETA_PROCESSED.mkdir(parents=True, exist_ok=True)


def cargar_datos() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga la tabla de ventas y las tres tablas maestras."""
    ventas = pd.read_csv(CARPETA_RAW / "ventas.csv")
    productos = pd.read_csv(CARPETA_RAW / "productos.csv")
    clientes = pd.read_csv(CARPETA_RAW / "clientes.csv")
    sucursales = pd.read_csv(CARPETA_RAW / "sucursales.csv")
    return ventas, productos, clientes, sucursales


def validar_clave_maestra(tabla: pd.DataFrame, clave: str, nombre: str) -> None:
    """Detiene el proceso si una dimensión tiene claves vacías o repetidas."""
    if tabla[clave].isna().any():
        raise ValueError(f"La tabla {nombre} contiene valores nulos en {clave}.")

    if tabla[clave].duplicated().any():
        raise ValueError(f"La tabla {nombre} contiene valores repetidos en {clave}.")


def main() -> None:
    ventas, productos, clientes, sucursales = cargar_datos()
    filas_originales = len(ventas)

    # Las claves de las tablas maestras deben identificar una sola fila.
    validar_clave_maestra(productos, "producto_id", "productos")
    validar_clave_maestra(clientes, "cliente_id", "clientes")
    validar_clave_maestra(sucursales, "sucursal_id", "sucursales")

    # errors="coerce" transforma valores imposibles en nulos para detectarlos.
    ventas["fecha"] = pd.to_datetime(ventas["fecha"], errors="coerce")

    columnas_numericas = [
        "cantidad",
        "precio_unitario",
        "descuento",
        "costo_unitario",
    ]
    for columna in columnas_numericas:
        ventas[columna] = pd.to_numeric(ventas[columna], errors="coerce")

    # Cada máscara es una serie de True/False: True significa "hay un problema".
    problemas = {
        "filas_duplicadas": ventas.duplicated(keep="first"),
        "fechas_invalidas": ventas["fecha"].isna(),
        "cantidades_invalidas": ventas["cantidad"].isna()
        | (ventas["cantidad"] <= 0),
        "precios_invalidos": ventas["precio_unitario"].isna()
        | (ventas["precio_unitario"] <= 0),
        "descuentos_invalidos": ventas["descuento"].isna()
        | ~ventas["descuento"].between(0, 1),
        "costos_invalidos": ventas["costo_unitario"].isna()
        | (ventas["costo_unitario"] <= 0),
        "productos_inexistentes": ~ventas["producto_id"].isin(
            productos["producto_id"]
        ),
        "clientes_inexistentes": ~ventas["cliente_id"].isin(
            clientes["cliente_id"]
        ),
        "sucursales_inexistentes": ~ventas["sucursal_id"].isin(
            sucursales["sucursal_id"]
        ),
    }

    # Una fila se elimina si presenta por lo menos uno de los problemas anteriores.
    fila_invalida = pd.Series(False, index=ventas.index)
    for mascara in problemas.values():
        fila_invalida = fila_invalida | mascara

    ventas_limpias = ventas.loc[~fila_invalida].copy()
    ventas_limpias["fecha"] = ventas_limpias["fecha"].dt.strftime("%Y-%m-%d")

    ruta_ventas = CARPETA_PROCESSED / "ventas_limpias.csv"
    ventas_limpias.to_csv(ruta_ventas, index=False)

    resumen = [
        {"metrica": "filas_originales", "cantidad": filas_originales},
        *[
            {"metrica": nombre, "cantidad": int(mascara.sum())}
            for nombre, mascara in problemas.items()
        ],
        {"metrica": "filas_eliminadas", "cantidad": int(fila_invalida.sum())},
        {"metrica": "filas_finales", "cantidad": len(ventas_limpias)},
    ]
    ruta_resumen = CARPETA_PROCESSED / "resumen_limpieza.csv"
    pd.DataFrame(resumen).to_csv(ruta_resumen, index=False)

    print("Limpieza y validación terminadas.")
    print(f"Filas originales: {filas_originales}")
    print(f"Filas eliminadas: {int(fila_invalida.sum())}")
    print(f"Filas finales: {len(ventas_limpias)}")
    print(f"Ventas limpias: {ruta_ventas}")
    print(f"Resumen: {ruta_resumen}")


if __name__ == "__main__":
    main()
