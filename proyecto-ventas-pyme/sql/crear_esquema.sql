PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS vw_ventas_detalle;
DROP TABLE IF EXISTS fact_ventas;
DROP TABLE IF EXISTS dim_productos;
DROP TABLE IF EXISTS dim_clientes;
DROP TABLE IF EXISTS dim_sucursales;

CREATE TABLE dim_productos (
    producto_id INTEGER PRIMARY KEY,
    producto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    costo_base REAL NOT NULL CHECK (costo_base > 0),
    precio_lista REAL NOT NULL CHECK (precio_lista > 0)
);

CREATE TABLE dim_clientes (
    cliente_id INTEGER PRIMARY KEY,
    cliente TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    provincia TEXT NOT NULL,
    segmento TEXT NOT NULL
);

CREATE TABLE dim_sucursales (
    sucursal_id INTEGER PRIMARY KEY,
    sucursal TEXT NOT NULL,
    ciudad TEXT NOT NULL
);

CREATE TABLE fact_ventas (
    venta_id INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    producto_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    sucursal_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL CHECK (precio_unitario > 0),
    descuento REAL NOT NULL CHECK (descuento BETWEEN 0 AND 1),
    costo_unitario REAL NOT NULL CHECK (costo_unitario > 0),
    FOREIGN KEY (producto_id) REFERENCES dim_productos (producto_id),
    FOREIGN KEY (cliente_id) REFERENCES dim_clientes (cliente_id),
    FOREIGN KEY (sucursal_id) REFERENCES dim_sucursales (sucursal_id)
);

CREATE INDEX idx_fact_ventas_fecha ON fact_ventas (fecha);
CREATE INDEX idx_fact_ventas_producto ON fact_ventas (producto_id);
CREATE INDEX idx_fact_ventas_cliente ON fact_ventas (cliente_id);
CREATE INDEX idx_fact_ventas_sucursal ON fact_ventas (sucursal_id);

CREATE VIEW vw_ventas_detalle AS
SELECT
    v.venta_id,
    v.fecha,
    CAST(strftime('%Y', v.fecha) AS INTEGER) AS anio,
    CAST(strftime('%m', v.fecha) AS INTEGER) AS mes,
    strftime('%Y-%m', v.fecha) AS periodo,
    p.producto,
    p.categoria,
    c.cliente,
    c.segmento,
    c.ciudad AS ciudad_cliente,
    c.provincia,
    s.sucursal,
    v.cantidad,
    v.precio_unitario,
    v.descuento,
    v.costo_unitario,
    ROUND(v.cantidad * v.precio_unitario, 2) AS venta_bruta,
    ROUND(v.cantidad * v.precio_unitario * (1 - v.descuento), 2) AS facturacion,
    ROUND(v.cantidad * v.costo_unitario, 2) AS costo_total,
    ROUND(
        v.cantidad * v.precio_unitario * (1 - v.descuento)
        - v.cantidad * v.costo_unitario,
        2
    ) AS margen
FROM fact_ventas AS v
INNER JOIN dim_productos AS p
    ON v.producto_id = p.producto_id
INNER JOIN dim_clientes AS c
    ON v.cliente_id = c.cliente_id
INNER JOIN dim_sucursales AS s
    ON v.sucursal_id = s.sucursal_id;
