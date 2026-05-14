import csv
from datetime import datetime
from uuid import UUID

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connect import get_cassandra

#conectar
cluster, session = get_cassandra()

session.set_keyspace("restaurante_db")

print("Conectado a Cassandra.")

#leer csv
with open("data/pedidos.csv", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)
#convertir tipos
    for row in reader:
        fecha_timestamp = datetime.fromisoformat(row["fecha"])

        fecha_date = fecha_timestamp.date()

        id_pedido = UUID(row["id_pedido"])

        total = float(row["total"])

        tiempo_entrega = int(row["tiempo_entrega"])

        distancia = float(row["distancia"])

        calificacion = int(row["calificacion"])

#tabla 1 pedidos por usuario
        session.execute("""
        INSERT INTO pedidos_por_usuario (
            usuario,
            fecha,
            id_pedido,
            restaurante,
            total,
            estado,
            repartidor,
            tiempo_entrega,
            distancia,
            calificacion
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["usuario"],
            fecha_timestamp,
            id_pedido,
            row["restaurante"],
            total,
            row["estado"],
            row["repartidor"],
            tiempo_entrega,
            distancia,
            calificacion
        ))
#tabla 2    
#pedidos por restaurante
        session.execute("""
        INSERT INTO pedidos_por_restaurante (
            restaurante,
            fecha,
            id_pedido,
            usuario,
            total,
            estado,
            metodo_pago
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["restaurante"],
            fecha_timestamp,
            id_pedido,
            row["usuario"],
            total,
            row["estado"],
            row["metodo_pago"]
        ))
#tabla 3 
#pedidos por fecha 
        session.execute("""
        INSERT INTO pedidos_por_fecha (
            fecha,
            id_pedido,
            usuario,
            restaurante,
            total,
            estado
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            fecha_date,
            id_pedido,
            row["usuario"],
            row["restaurante"],
            total,
            row["estado"]
        ))

#tabla 4
#pedidos por repartidor
        session.execute("""
        INSERT INTO pedidos_por_repartidor (
            repartidor,
            fecha,
            id_pedido,
            restaurante,
            estado,
            distancia,
            tiempo_entrega,
            calificacion,
            zona
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["repartidor"],
            fecha_timestamp,
            id_pedido,
            row["restaurante"],
            row["estado"],
            distancia,
            tiempo_entrega,
            calificacion,
            row["zona"]
        ))

#Tabla 5
#pedidos por zona restaurante
        session.execute("""
        INSERT INTO pedidos_por_zona_restaurante (
            zona,
            restaurante,
            fecha,
            id_pedido,
            usuario,
            total,
            direccion
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["zona"],
            row["restaurante"],
            fecha_timestamp,
            id_pedido,
            row["usuario"],
            total,
            row["direccion"]
        ))

#tabla 6
#entregas por paqueteria
        session.execute("""
        INSERT INTO entregas_por_paqueteria (
            tipo_paqueteria,
            fecha,
            id_pedido,
            repartidor,
            restaurante,
            tiempo_entrega,
            distancia
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["tipo_paqueteria"],
            fecha_timestamp,
            id_pedido,
            row["repartidor"],
            row["restaurante"],
            tiempo_entrega,
            distancia
        ))
#tabla 7
#pedidos por categoria
        session.execute("""
        INSERT INTO pedidos_por_categoria (
            categoria,
            fecha,
            id_pedido,
            restaurante,
            usuario,
            total,
            estado
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["categoria"],
            fecha_timestamp,
            id_pedido,
            row["restaurante"],
            row["usuario"],
            total,
            row["estado"]
        ))

print("Datos insertados correctamente en Cassandra.")

#cerrrar la conexion 
cluster.shutdown()