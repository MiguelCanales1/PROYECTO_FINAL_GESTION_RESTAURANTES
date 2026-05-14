import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connect import get_cassandra

# Conexion a Cassandra
cluster, session = get_cassandra()

# Crear keyspace
session.execute("""
CREATE KEYSPACE IF NOT EXISTS restaurante_db
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};
""")

# Seleccionar keyspace
session.set_keyspace('restaurante_db')

# =========================
# TABLA 1 - Pedidos por usuario
# =========================
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_usuario (
    usuario TEXT,
    fecha TIMESTAMP,
    id_pedido UUID,
    restaurante TEXT,
    total DECIMAL,
    estado TEXT,
    repartidor TEXT,
    tiempo_entrega INT,
    distancia DECIMAL,
    calificacion INT,
    PRIMARY KEY ((usuario), fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

# =========================
# TABLA 2 - Pedidos por restaurante
# =========================
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_restaurante (
    restaurante TEXT,
    fecha TIMESTAMP,
    id_pedido UUID,
    usuario TEXT,
    total DECIMAL,
    estado TEXT,
    metodo_pago TEXT,
    PRIMARY KEY ((restaurante), fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

# =========================
# TABLA 3 - Pedidos por fecha
# =========================
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_fecha (
    fecha DATE,
    id_pedido UUID,
    usuario TEXT,
    restaurante TEXT,
    total DECIMAL,
    estado TEXT,
    PRIMARY KEY ((fecha), id_pedido)
);
""")

# =========================
# TABLA 4 - Pedidos por repartidor
# =========================
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_repartidor (
    repartidor TEXT,
    fecha TIMESTAMP,
    id_pedido UUID,
    restaurante TEXT,
    estado TEXT,
    distancia DECIMAL,
    tiempo_entrega INT,
    calificacion INT,
    zona TEXT,
    PRIMARY KEY ((repartidor), fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

# =========================
# TABLA 5 - Pedidos por zona y restaurante
# =========================
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_zona_restaurante (
    zona TEXT,
    restaurante TEXT,
    fecha TIMESTAMP,
    id_pedido UUID,
    usuario TEXT,
    total DECIMAL,
    direccion TEXT,
    PRIMARY KEY ((zona, restaurante), fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

# =========================
# TABLA 6 - Entregas por paqueteria
# =========================
session.execute("""
CREATE TABLE IF NOT EXISTS entregas_por_paqueteria (
    tipo_paqueteria TEXT,
    fecha TIMESTAMP,
    id_pedido UUID,
    repartidor TEXT,
    restaurante TEXT,
    tiempo_entrega INT,
    distancia DECIMAL,
    PRIMARY KEY ((tipo_paqueteria), fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

#tabla pedidos por categoria
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_categoria (
    categoria TEXT,
    fecha TIMESTAMP,
    id_pedido UUID,
    restaurante TEXT,
    usuario TEXT,
    total DECIMAL,
    estado TEXT,
    PRIMARY KEY ((categoria), fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

print("Keyspace y tablas creadas correctamente.")

# Cerrar conexion
cluster.shutdown()