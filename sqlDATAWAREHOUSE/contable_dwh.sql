CREATE DATABASE contable_dwh;
USE contable_dwh;

CREATE TABLE dim_tiempo (
    id_fecha INT PRIMARY KEY,
    fecha DATE,
    anio INT,
    mes INT,
    nombre_mes VARCHAR(20),
    trimestre INT
);

CREATE TABLE dim_tercero (
    id_tercero INT PRIMARY KEY AUTO_INCREMENT,
    nit VARCHAR(20),
    razon_social VARCHAR(150),
    tipo_tercero VARCHAR(20) 
);

CREATE TABLE dim_punto_venta (
    id_punto_venta INT PRIMARY KEY AUTO_INCREMENT,
    nombre_sucursal VARCHAR(100),
    ciudad VARCHAR(50)
);

CREATE TABLE dim_tipo_factura (
    id_tipo_factura INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(50)
);

CREATE TABLE hechos_transacciones (
    id_transaccion INT PRIMARY KEY AUTO_INCREMENT,
    id_fecha INT,
    id_tercero INT,
    id_punto_venta INT,
    id_tipo_factura INT,
    tipo_operacion VARCHAR(20), 
    monto_total DECIMAL(12,2),
    monto_neto DECIMAL(12,2),
    impuestos DECIMAL(12,2),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo(id_fecha),
    FOREIGN KEY (id_tercero) REFERENCES dim_tercero(id_tercero),
    FOREIGN KEY (id_punto_venta) REFERENCES dim_punto_venta(id_punto_venta),
    FOREIGN KEY (id_tipo_factura) REFERENCES dim_tipo_factura(id_tipo_factura)
);