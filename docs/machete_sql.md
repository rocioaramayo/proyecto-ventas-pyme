# Machete de SQL

## Orden mental de una consulta

Aunque `SELECT` se escribe primero, SQL procesa conceptualmente una consulta así:

```text
FROM y JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

## SELECT: elegir columnas

```sql
SELECT producto, categoria, facturacion
FROM vw_ventas_detalle;
```

`SELECT` indica qué información querés ver y `FROM` de qué tabla sale.

## WHERE: filtrar filas

```sql
SELECT *
FROM vw_ventas_detalle
WHERE facturacion > 100000;
```

`WHERE` se aplica antes de agrupar.

## JOIN: relacionar tablas

```sql
SELECT v.venta_id, p.producto
FROM fact_ventas AS v
INNER JOIN dim_productos AS p
    ON v.producto_id = p.producto_id;
```

La lógica es buscar en ambas tablas las filas que tengan el mismo `producto_id`.

## GROUP BY: resumir

```sql
SELECT
    categoria,
    SUM(facturacion) AS facturacion
FROM vw_ventas_detalle
GROUP BY categoria;
```

`GROUP BY` reúne las filas de una misma categoría. `SUM` calcula un resultado para cada grupo.

Funciones frecuentes:

- `SUM`: suma.
- `COUNT`: cantidad de filas.
- `AVG`: promedio.
- `MIN`: valor mínimo.
- `MAX`: valor máximo.

## CASE: crear categorías

```sql
CASE
    WHEN descuento = 0 THEN 'Sin descuento'
    WHEN descuento <= 0.10 THEN 'Hasta 10%'
    ELSE 'Más de 10%'
END
```

Funciona como un `if / elif / else` de Python.

## CTE: crear un resultado temporal

```sql
WITH ventas_mensuales AS (
    SELECT periodo, SUM(facturacion) AS facturacion
    FROM vw_ventas_detalle
    GROUP BY periodo
)
SELECT *
FROM ventas_mensuales;
```

La CTE permite dividir una consulta compleja en pasos con nombre.

## Funciones de ventana

```sql
LAG(facturacion) OVER (ORDER BY periodo)
```

`LAG` trae el valor de la fila anterior sin agrupar ni eliminar filas. En este proyecto permite comparar cada mes con el anterior.

```sql
DENSE_RANK() OVER (
    PARTITION BY categoria
    ORDER BY facturacion DESC
)
```

- `PARTITION BY`: reinicia el ranking para cada categoría.
- `ORDER BY`: decide qué producto ocupa la primera posición.

## Evitar divisiones por cero

```sql
margen / NULLIF(facturacion, 0)
```

`NULLIF(facturacion, 0)` devuelve `NULL` cuando la facturación es cero y evita que la consulta falle.

## Ejecutar el proyecto

```powershell
python src/limpieza.py
python src/cargar_sqlite.py
```

La base resultante queda en `data/processed/ventas_pyme.db` y las consultas se encuentran en `sql/analisis_ventas.sql`.
