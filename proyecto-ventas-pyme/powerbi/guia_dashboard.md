# Guía para construir el dashboard en Power BI

## 1. Importar los datos

En Power BI Desktop, seleccionar **Obtener datos → Texto/CSV** e importar:

1. `data/processed/ventas_limpias.csv`
2. `data/raw/productos.csv`
3. `data/raw/clientes.csv`
4. `data/raw/sucursales.csv`

En Power Query, renombrar las consultas:

| Archivo | Nombre en Power BI |
| --- | --- |
| `ventas_limpias.csv` | `FactVentas` |
| `productos.csv` | `DimProducto` |
| `clientes.csv` | `DimCliente` |
| `sucursales.csv` | `DimSucursal` |

Comprobar los tipos:

- `fecha`: Fecha.
- Identificadores y `cantidad`: Número entero.
- Precios, costos y `descuento`: Número decimal.
- Nombres, ciudades, provincias, categorías y segmentos: Texto.

Después seleccionar **Cerrar y aplicar**.

## 2. Construir el modelo estrella

En la vista Modelo, crear relaciones de uno a muchos:

```text
DimProducto[producto_id]  1 ───── * FactVentas[producto_id]
DimCliente[cliente_id]    1 ───── * FactVentas[cliente_id]
DimSucursal[sucursal_id]  1 ───── * FactVentas[sucursal_id]
DimFecha[Fecha]           1 ───── * FactVentas[fecha]
```

Usar dirección de filtro única desde las dimensiones hacia `FactVentas`.

No relacionar las dimensiones entre sí.

## 3. Crear la tabla calendario y las medidas

Copiar el código de `powerbi/medidas_dax.txt` desde **Modelado → Nueva tabla** y **Modelado → Nueva medida**.

Formatos:

- Facturación, venta bruta, descuentos, costo, margen y ticket: Moneda.
- Margen %, crecimiento % y participación: Porcentaje con dos decimales.
- Unidades, ventas y clientes: Número entero.

Los resultados principales deben aproximarse a:

| Medida | Resultado de control |
| --- | ---: |
| Cantidad de ventas | 1.195 |
| Facturación | $182.490.551,03 |
| Margen | $50.098.827,98 |
| Ticket promedio | $152.711,76 |

Si no coinciden, revisar los tipos de datos, las relaciones o la fórmula del descuento.

## 4. Página 1: Resumen ejecutivo

### Encabezado

Título: **Análisis de ventas de una pyme**

Subtítulo: **Enero 2025 – Agosto 2026**

### Tarjetas superiores

1. Facturación.
2. Margen.
3. Margen %.
4. Ticket promedio.
5. Cantidad de ventas.

### Visuales

- Gráfico de líneas: `DimFecha[Año-Mes]` y `[Facturación]`.
- Gráfico de barras: `DimProducto[categoria]` y `[Facturación]`.
- Gráfico de columnas: `DimSucursal[sucursal]` y `[Facturación]`.
- Segmentadores: Fecha, categoría, sucursal y segmento.

## 5. Página 2: Productos y clientes

- Barras horizontales: diez productos por facturación.
- Matriz: categoría, producto, unidades, facturación, margen y margen %.
- Barras: segmento de cliente por facturación.
- Tabla: clientes principales, cantidad de ventas, facturación y margen.
- Segmentadores: categoría, segmento y provincia.

## 6. Diseño

Importar `powerbi/tema_lila.json` desde **Vista → Temas → Examinar temas**.

Reglas visuales:

- Utilizar fondo claro.
- Mantener el lila como color principal y reservar otros colores para comparaciones.
- No usar gráficos 3D.
- No colocar más de seis visuales principales por página.
- Alinear los elementos y mantener espacios consistentes.
- Escribir títulos que expliquen la métrica, no títulos genéricos como “Gráfico 1”.

## 7. Guardar y documentar

Guardar el archivo como:

```text
powerbi/ventas_pyme_dashboard.pbix
```

Exportar capturas de las dos páginas y guardarlas dentro de `images/`.
