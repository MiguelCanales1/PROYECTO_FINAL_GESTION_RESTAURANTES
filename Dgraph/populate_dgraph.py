import sys
import os
import csv
import pydgraph
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connect import get_dgraph
from Dgraph.model import create_schema

stub, client = get_dgraph()

# Limpiar base de datos antes de cargar
client.alter(pydgraph.Operation(drop_all=True))
create_schema()

data = []

with open("data/pedidos.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        # Generar UIDs basados en nombres y zonas para evitar colisiones
        user_id_clean = r['usuario'].replace(' ', '_')
        rest_id_clean = f"{r['restaurante']}_{r['zona']}".replace(' ', '_')
        
        user_uid = f"_:{user_id_clean}"
        rest_uid = f"_:{rest_id_clean}"
        order_uid = f"_:{r['id_pedido']}"
        driver_uid = f"_:{r['repartidor'].replace(' ', '_')}"
        dish_uid = f"_:{r['platillo'].replace(' ', '_')}"

        # Estructura del Usuario
        user_node = {
            "uid": user_uid,
            "dgraph.type": "Usuario",
            "user_id": r["usuario"],
            "user_name": r["usuario"],
            "zone": r["zona"],
            "PLACES": [
                {
                    "uid": order_uid,
                    "dgraph.type": "Pedido",
                    "order_id": r["id_pedido"],
                    "order_date": r["fecha"].replace(" ", "T"),
                    "FROM": [{"uid": rest_uid}],
                    "CONTAINS": [{
                        "uid": dish_uid,
                        "dgraph.type": "Platillo",
                        "dish_id": r["platillo"],
                        "dish_name": r["platillo"],
                        "category": r["categoria"]
                    }]
                }
            ]
        }

        # Solo agregar a FAVORITE si la calificación es 5
        if r.get("calificacion") == "5":
            user_node["FAVORITE"] = [{"uid": rest_uid}]
        
        data.append(user_node)

        # Repartidor y sus relaciones
        data.append({
            "uid": driver_uid,
            "dgraph.type": "Repartidor",
            "driver_id": r["repartidor"],
            "driver_name": r["repartidor"],
            "DELIVERS": [{"uid": order_uid}],
            "WORKS_IN": [{"uid": rest_uid}]
        })

        # Restaurante (asegurar que existe y tiene el platillo)
        data.append({
            "uid": rest_uid,
            "dgraph.type": "Restaurante",
            "restaurant_id": r["restaurante"],
            "restaurant_name": r["restaurante"],
            "category": r["categoria_restaurante"],
            "zone": r["zona"],
            "address": r["direccion"],
            "SERVES": [{"uid": dish_uid}]
        })

txn = client.txn()
try:
    txn.mutate(set_obj=data)
    txn.commit()
    print("Datos insertados en Dgraph con platillos")
finally:
    txn.discard()
    stub.close()