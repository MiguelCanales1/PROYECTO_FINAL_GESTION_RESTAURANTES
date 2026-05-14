import csv
from pymongo import MongoClient
from datetime import datetime
from connect import get_mongodb

client, db, coll = get_mongodb()
print("Eliminar documentos anteriores...")
coll.delete_many({})

print("Creando indices...")


print("Lectura del archivo CSV....")
data = []
with open("../data/pedidos.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        documento = {
            "orderID": r["id_pedido"],
            "customerName": r["usuario"],
            "orderPrice": float(r["total"]),
            "orderDate": datetime.strptime(r["fecha"].split('.')[0], "%Y-%m-%d %H:%M:%S"),
            "restaurantName": r["restaurante"],
            "delivererName": r["repartidor"],
            "deliveryAddress": r["direccion"],
            "postCode": r["zona"],
            "deliveryTime": int(r["tiempo_entrega"]),
            "deliveryDistance": float(r["distancia"]),
            "deliveryRating": int(r["calificacion"])
        }
        data.append(documento)

if data:
    coll.insert_many(data)
    print(f"Se insertaron {len(data)} documentos.")
