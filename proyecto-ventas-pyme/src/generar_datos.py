from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
CARPETA_RAW = RAIZ / "data" / "raw"
SEMILLA = 42


def guardar_csv(nombre: str, columnas: list[str], filas: list[dict]) -> None:
    ruta = CARPETA_RAW / nombre
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"Creado: {ruta} ({len(filas)} filas)")


def fecha_aleatoria(inicio: date, fin: date) -> date:
    diferencia = (fin - inicio).days
    return inicio + timedelta(days=random.randint(0, diferencia))


def main() -> None:
    random.seed(SEMILLA)
    CARPETA_RAW.mkdir(parents=True, exist_ok=True)

    categorias = {
        "Tecnologia": ["Teclado", "Mouse", "Auriculares", "Monitor", "Webcam"],
        "Oficina": ["Cuaderno", "Agenda", "Lapicera", "Resaltador", "Carpeta"],
        "Hogar": ["Lampara", "Organizador", "Botella", "Taza", "Almohadon"],
        "Accesorios": ["Mochila", "Soporte notebook", "Cable USB", "Cargador", "Funda"],
        "Libreria": ["Libro", "Calculadora", "Regla", "Tijera", "Notas adhesivas"],
    }

    productos = []
    producto_id = 1
    for categoria, nombres in categorias.items():
        for nombre in nombres:
            costo = round(random.uniform(800, 45000), 2)
            precio = round(costo * random.uniform(1.25, 1.85), 2)
            productos.append(
                {
                    "producto_id": producto_id,
                    "producto": nombre,
                    "categoria": categoria,
                    "costo_base": costo,
                    "precio_lista": precio,
                }
            )
            producto_id += 1

    ciudades = [
        ("CABA", "Buenos Aires"),
        ("La Plata", "Buenos Aires"),
        ("Mar del Plata", "Buenos Aires"),
        ("Cordoba", "Cordoba"),
        ("Rosario", "Santa Fe"),
        ("Mendoza", "Mendoza"),
    ]
    clientes = []
    for cliente_id in range(1, 181):
        ciudad, provincia = random.choice(ciudades)
        clientes.append(
            {
                "cliente_id": cliente_id,
                "cliente": f"Cliente {cliente_id:03d}",
                "ciudad": ciudad,
                "provincia": provincia,
                "segmento": random.choice(["Minorista", "Pyme", "Profesional"]),
            }
        )

    sucursales = [
        {"sucursal_id": 1, "sucursal": "Centro", "ciudad": "CABA"},
        {"sucursal_id": 2, "sucursal": "Norte", "ciudad": "Vicente Lopez"},
        {"sucursal_id": 3, "sucursal": "Online", "ciudad": "CABA"},
    ]

    inicio = date(2025, 1, 1)
    fin = date(2026, 8, 31)
    descuentos = [0, 0, 0, 0.05, 0.10, 0.15, 0.20]
    ventas = []

    for venta_id in range(1, 1201):
        producto = random.choice(productos)
        precio = round(
            producto["precio_lista"] * random.uniform(0.95, 1.08), 2
        )
        costo = round(
            producto["costo_base"] * random.uniform(0.97, 1.06), 2
        )
        ventas.append(
            {
                "venta_id": venta_id,
                "fecha": fecha_aleatoria(inicio, fin).isoformat(),
                "producto_id": producto["producto_id"],
                "cliente_id": random.randint(1, len(clientes)),
                "sucursal_id": random.randint(1, len(sucursales)),
                "cantidad": random.randint(1, 8),
                "precio_unitario": precio,
                "descuento": random.choice(descuentos),
                "costo_unitario": costo,
            }
        )

    # Errores intencionales para practicar validacion y limpieza.
    ventas[25]["cantidad"] = -2
    ventas[90]["precio_unitario"] = 0
    ventas[145]["descuento"] = 1.25
    ventas[210]["fecha"] = "fecha-invalida"
    ventas[330]["precio_unitario"] = ""
    ventas.extend([ventas[50].copy(), ventas[400].copy(), ventas[750].copy()])

    guardar_csv(
        "productos.csv",
        ["producto_id", "producto", "categoria", "costo_base", "precio_lista"],
        productos,
    )
    guardar_csv(
        "clientes.csv",
        ["cliente_id", "cliente", "ciudad", "provincia", "segmento"],
        clientes,
    )
    guardar_csv(
        "sucursales.csv",
        ["sucursal_id", "sucursal", "ciudad"],
        sucursales,
    )
    guardar_csv(
        "ventas.csv",
        [
            "venta_id",
            "fecha",
            "producto_id",
            "cliente_id",
            "sucursal_id",
            "cantidad",
            "precio_unitario",
            "descuento",
            "costo_unitario",
        ],
        ventas,
    )


if __name__ == "__main__":
    main()
