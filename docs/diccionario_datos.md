# Diccionario de datos

El conjunto de datos es sintético y representa las ventas de una pyme entre enero de 2025 y agosto de 2026.

## FactVentas

Archivo procesado: `data/processed/ventas_limpias.csv`

| Campo | Tipo esperado | Descripción |
| --- | --- | --- |
| `venta_id` | Entero | Identificador de la venta. |
| `fecha` | Fecha | Fecha en la que se realizó la venta. |
| `producto_id` | Entero | Clave que relaciona la venta con `DimProducto`. |
| `cliente_id` | Entero | Clave que relaciona la venta con `DimCliente`. |
| `sucursal_id` | Entero | Clave que relaciona la venta con `DimSucursal`. |
| `cantidad` | Entero | Unidades vendidas. Debe ser mayor que cero. |
| `precio_unitario` | Decimal | Precio por unidad antes del descuento. |
| `descuento` | Decimal | Descuento expresado entre 0 y 1. Por ejemplo, `0.10` equivale al 10 %. |
| `costo_unitario` | Decimal | Costo unitario para la empresa. |

## DimProducto

Archivo: `data/raw/productos.csv`

| Campo | Tipo esperado | Descripción |
| --- | --- | --- |
| `producto_id` | Entero | Identificador único del producto. |
| `producto` | Texto | Nombre del producto. |
| `categoria` | Texto | Categoría comercial del producto. |
| `costo_base` | Decimal | Costo de referencia del producto. |
| `precio_lista` | Decimal | Precio de lista del producto. |

## DimCliente

Archivo: `data/raw/clientes.csv`

| Campo | Tipo esperado | Descripción |
| --- | --- | --- |
| `cliente_id` | Entero | Identificador único del cliente. |
| `cliente` | Texto | Nombre anonimizado del cliente. |
| `ciudad` | Texto | Ciudad del cliente. |
| `provincia` | Texto | Provincia del cliente. |
| `segmento` | Texto | Segmento comercial: Minorista, Pyme o Profesional. |

## DimSucursal

Archivo: `data/raw/sucursales.csv`

| Campo | Tipo esperado | Descripción |
| --- | --- | --- |
| `sucursal_id` | Entero | Identificador único de la sucursal. |
| `sucursal` | Texto | Nombre de la sucursal o canal. |
| `ciudad` | Texto | Ciudad asociada a la sucursal. |

## Relaciones esperadas

- `FactVentas.producto_id` → `DimProducto.producto_id`
- `FactVentas.cliente_id` → `DimCliente.cliente_id`
- `FactVentas.sucursal_id` → `DimSucursal.sucursal_id`

En Power BI estas relaciones deben ser de uno a muchos, desde cada dimensión hacia `FactVentas`.
