from pathlib import Path
import sqlite3

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
CARPETA_RAW = RAIZ / "data" / "raw"
CARPETA_PROCESSED = RAIZ / "data" / "processed"
RUTA_BASE = CARPETA_PROCESSED / "ventas_pyme.db"
RUTA_ESQUEMA = RAIZ / "sql" / "crear_esquema.sql"


def cargar_csv(nombre: str, carpeta: Path = CARPETA_RAW) -> pd.DataFrame:
    """Lee un CSV y devuelve una tabla de pandas."""
    return pd.read_csv(carpeta / nombre)


def main() -> None:
    productos = cargar_csv("productos.csv")
    clientes = cargar_csv("clientes.csv")
    sucursales = cargar_csv("sucursales.csv")
    ventas = cargar_csv("ventas_limpias.csv", CARPETA_PROCESSED)

    CARPETA_PROCESSED.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(RUTA_BASE) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON;")
        conexion.executescript(RUTA_ESQUEMA.read_text(encoding="utf-8"))

        # append inserta las filas en las tablas creadas por crear_esquema.sql.
        productos.to_sql("dim_productos", conexion, if_exists="append", index=False)
        clientes.to_sql("dim_clientes", conexion, if_exists="append", index=False)
        sucursales.to_sql("dim_sucursales", conexion, if_exists="append", index=False)
        ventas.to_sql("fact_ventas", conexion, if_exists="append", index=False)

        cantidades = conexion.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM fact_ventas),
                (SELECT COUNT(*) FROM dim_productos),
                (SELECT COUNT(*) FROM dim_clientes),
                (SELECT COUNT(*) FROM dim_sucursales)
            """
        ).fetchone()

    print(f"Base creada: {RUTA_BASE}")
    print(f"Ventas: {cantidades[0]}")
    print(f"Productos: {cantidades[1]}")
    print(f"Clientes: {cantidades[2]}")
    print(f"Sucursales: {cantidades[3]}")


if __name__ == "__main__":
    main()
