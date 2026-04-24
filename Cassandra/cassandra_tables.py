
#tabla 1 pedidos por usuario
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_usuario (
    id_usuario UUID,
    fecha TIMESTAMP,
    id_pedido UUID,
    restaurante TEXT,
    total DECIMAL,
    estado TEXT,
    PRIMARY KEY (id_usuario, fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")

#tabla 2 pedidos por repartidor
session.execute("""
CREATE TABLE IF NOT EXISTS pedidos_por_repartidor (
    id_repartidor UUID,
    fecha TIMESTAMP,
    id_pedido UUID,
    restaurante TEXT,
    distancia DECIMAL,
    tiempo_entrega INT,
    PRIMARY KEY (id_repartidor, fecha, id_pedido)
) WITH CLUSTERING ORDER BY (fecha DESC);
""")