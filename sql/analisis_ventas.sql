-- ============================================================
-- PROYECTO: Análisis de ventas de una pyme
-- Base: data/processed/ventas_pyme.db
-- Motor: SQLite
-- ============================================================

-- 1. KPI generales
SELECT
    COUNT(*) AS cantidad_ventas,
    SUM(cantidad) AS unidades_vendidas,
    ROUND(SUM(facturacion), 2) AS facturacion_total,
    ROUND(SUM(costo_total), 2) AS costo_total,
    ROUND(SUM(margen), 2) AS margen_total,
    ROUND(AVG(facturacion), 2) AS ticket_promedio,
    ROUND(100.0 * SUM(margen) / NULLIF(SUM(facturacion), 0), 2) AS margen_porcentaje
FROM vw_ventas_detalle;

-- 2. Evolución mensual
SELECT
    periodo,
    COUNT(*) AS cantidad_ventas,
    SUM(cantidad) AS unidades,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(SUM(margen), 2) AS margen
FROM vw_ventas_detalle
GROUP BY periodo
ORDER BY periodo;

-- 3. Crecimiento mensual usando una CTE y LAG
WITH ventas_mensuales AS (
    SELECT
        periodo,
        SUM(facturacion) AS facturacion
    FROM vw_ventas_detalle
    GROUP BY periodo
),
comparacion AS (
    SELECT
        periodo,
        facturacion,
        LAG(facturacion) OVER (ORDER BY periodo) AS facturacion_mes_anterior
    FROM ventas_mensuales
)
SELECT
    periodo,
    ROUND(facturacion, 2) AS facturacion,
    ROUND(facturacion_mes_anterior, 2) AS facturacion_mes_anterior,
    ROUND(
        100.0 * (facturacion - facturacion_mes_anterior)
        / NULLIF(facturacion_mes_anterior, 0),
        2
    ) AS crecimiento_porcentaje
FROM comparacion
ORDER BY periodo;

-- 4. Rendimiento por categoría
SELECT
    categoria,
    SUM(cantidad) AS unidades,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(SUM(margen), 2) AS margen,
    ROUND(100.0 * SUM(margen) / NULLIF(SUM(facturacion), 0), 2) AS margen_porcentaje
FROM vw_ventas_detalle
GROUP BY categoria
ORDER BY facturacion DESC;

-- 5. Los diez productos con mayor facturación
SELECT
    producto,
    categoria,
    SUM(cantidad) AS unidades,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(SUM(margen), 2) AS margen
FROM vw_ventas_detalle
GROUP BY producto, categoria
ORDER BY facturacion DESC
LIMIT 10;

-- 6. Ranking de productos dentro de cada categoría
WITH ventas_producto AS (
    SELECT
        categoria,
        producto,
        SUM(facturacion) AS facturacion
    FROM vw_ventas_detalle
    GROUP BY categoria, producto
),
ranking AS (
    SELECT
        categoria,
        producto,
        facturacion,
        DENSE_RANK() OVER (
            PARTITION BY categoria
            ORDER BY facturacion DESC
        ) AS posicion
    FROM ventas_producto
)
SELECT
    categoria,
    posicion,
    producto,
    ROUND(facturacion, 2) AS facturacion
FROM ranking
WHERE posicion <= 3
ORDER BY categoria, posicion;

-- 7. Rendimiento por sucursal
SELECT
    sucursal,
    COUNT(*) AS cantidad_ventas,
    SUM(cantidad) AS unidades,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(AVG(facturacion), 2) AS ticket_promedio,
    ROUND(SUM(margen), 2) AS margen
FROM vw_ventas_detalle
GROUP BY sucursal
ORDER BY facturacion DESC;

-- 8. Rendimiento por segmento de cliente
SELECT
    segmento,
    COUNT(DISTINCT cliente) AS clientes,
    COUNT(*) AS cantidad_ventas,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(AVG(facturacion), 2) AS ticket_promedio,
    ROUND(SUM(margen), 2) AS margen
FROM vw_ventas_detalle
GROUP BY segmento
ORDER BY facturacion DESC;

-- 9. Los diez clientes con mayor facturación
SELECT
    cliente,
    segmento,
    provincia,
    COUNT(*) AS cantidad_ventas,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(SUM(margen), 2) AS margen
FROM vw_ventas_detalle
GROUP BY cliente, segmento, provincia
ORDER BY facturacion DESC
LIMIT 10;

-- 10. Impacto de los descuentos
SELECT
    CASE
        WHEN descuento = 0 THEN 'Sin descuento'
        WHEN descuento <= 0.10 THEN 'Hasta 10%'
        ELSE 'Más de 10%'
    END AS rango_descuento,
    COUNT(*) AS cantidad_ventas,
    ROUND(SUM(venta_bruta - facturacion), 2) AS importe_descontado,
    ROUND(SUM(facturacion), 2) AS facturacion,
    ROUND(SUM(margen), 2) AS margen
FROM vw_ventas_detalle
GROUP BY rango_descuento
ORDER BY facturacion DESC;
