# Este archivo se encargara de plobar las 3 base de datos que son:
# Cassandra, MongoDB y Dgraph de datos generados tomando como ejemplo Faker o CSV
# La idea es poder simular pedidos de una aplicacion de delivery muy similar a Rappi, Didi y Uber Eats
# El flujo general es generar datos (usuarios, pedidos, restaurantes, repartidores), de ahi transformarlos
# segun la estructura de cada base de datos y ya luego insertarlos recpectivamente.

#---------------------------------------------------------------------------------------------------------
#Cassandra
#En cassandra no se insertan datos genericos, porque se modelan en funcion de los queries, por lo tanto 
#los mismos datos se insertan en diferentes tablas.

#Un ejemplo
#Oder_by_user satisface los requerimientos 1 y 2
#Insercion: Cada pedido generado, se insertara un registro en esa tabla utilizando como partition key:
#user_name y clustering key: order_date
#Justificacion: Esto permite obtener rapidamente los pedidos de un usuario ordenados por fecha

#---------------------------------------------------------------------------------------------------------
#MongoDb
#Aqui la insercion sera directa, ya que con una sola coleccion se pueden obtener todos los requerimientos
#por ende cada documento representa un pedido completo con toda la informacion necesaria.
#La estructura de la coleccion de pedidos sera...
#Ejemplo de documento que se insertará:
# {
#  "_id": "OrderID",
#  "CustomerName": "String",
#  "OrderPrice": Float,
#  "orderDate": Date,
#  "RestaurantName": "String",
#  "DelivererName": "String",
#  "DeliveryAddress": "String",
#  "PostCode": Int,
#  "DeliveryTime": Int,
#  "DeliveryDistance": Float,
#  "DeliveryRating": Int
# }

#La implementacion sera generando multiples pedidos con valores aleatorios(delimitados para coincidencia
# de datos) usnado insert_many

#---------------------------------------------------------------------------------------------------------
#Dgraph
#La implemantacion sera la creacion de los nodos:
#  Usuario
#  Restaurante
#  Platillo
#  Pedido
#  Repartidor

#Posteriormente las relaciones entre ellos..
# FAVORITE: Usuario -> Restaurante
# PLACES: Usuario -> Pedido
# FROM: Pedido -> Restaurante
# CONTAINS: Pedido -> Platillo
# DELIVERS: Repartidor -> Pedido
# WORKS_IN: Repartidor -> Restaurante
# SERVES: Restaurante -> Platillo

#Y un ejemplo de insercion
#{
#  "uid": "_:user1",
#  "user_id": "U1",
#  "user_name": "Angel",
#  "PLACES": {
#    "uid": "_:order1",
#    "order_id": "O1",
#    "FROM": {
#      "uid": "_:restaurant1",
#       "restaurant_name": "McDonalds"
#    }
#  }
#}

from pymongo import MongoClient
from datetime import datetime
from connect import get_mongodb

import csv
import pydgraph
# MongoDB
client, db, coll = get_mongodb
print("Eliminar documentos anteriores...")
coll.delete_many({})
print("Lectura del archivo CSV....")
data = []
with open("data/pedidos.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        documento = {
            "orderID",
            "customerName",
            "orderPrice",
            "orderDate",
            "restaurantName",
            "delivererName",
            "deliveryAddress",
            "postCode",
            "deliveryTime",
            "deliveryDistance",
            "deliveryRating"
        }
# Dgraph
def load_data(client):

    data = []

    with open("data/users.csv", encoding="utf-8") as f:

        for r in csv.DictReader(f):

            data.append({
                "uid": f"_:{r['user_id']}",
                "dgraph.type": "Usuario",

                "user_id": r["user_id"],
                "user_name": r["user_name"],
                "zone": r["zone"],
                "address": r["address"],
                "postal_code": int(r["postal_code"])
            })

    with open("data/restaurants.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            data.append({
                "uid": f"_:{r['restaurant_id']}",
                "dgraph.type": "Restaurante",
                "restaurant_id": r["restaurant_id"],
                "restaurant_name": r["restaurant_name"],
                "category": r["category"],
                "zone": r["zone"],
                "address": r["address"]
            })

    with open("data/dishes.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            data.append({
                "uid": f"_:{r['dish_id']}",
                "dgraph.type": "Platillo",
                "dish_id": r["dish_id"],
                "dish_name": r["dish_name"],
                "category": r["category"],
                "price": float(r["price"]),
                "served_by": [{
                    "uid": f"_:{r['restaurant_id']}"
                }]
            })

    with open("data/drivers.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            data.append({
                "uid": f"_:{r['driver_id']}",
                "dgraph.type": "Repartidor",
                "driver_id": r["driver_id"],
                "driver_name": r["driver_name"],
                "zone": r["zone"],
                "delivery_company": r["delivery_company"]
            })

    with open("data/orders.csv", encoding="utf-8") as f:

        for r in csv.DictReader(f):

            data.append({
                "uid": f"_:{r['order_id']}",
                "dgraph.type": "Pedido",
                "order_id": r["order_id"],
                "order_date": r["order_date"],
                "total": float(r["total"]),
                "status": r["status"],
                "payment_method": r["payment_method"],
                "delivery_time": int(r["delivery_time"]),
                "delivery_distance": float(r["delivery_distance"]),
                "delivery_rating": int(r["delivery_rating"]),
                "delivery_company": r["delivery_company"],
                "delivery_zone": r["delivery_zone"],
                "ordered_by": [{
                    "uid": f"_:{r['user_id']}"
                }],

                "from_restaurant": [{
                    "uid": f"_:{r['restaurant_id']}"
                }],

                "delivered_by": [{
                    "uid": f"_:{r['driver_id']}"
                }]
            })

    with open("data/order_items.csv", encoding="utf-8") as f:

        for r in csv.DictReader(f):

            data.append({
                "uid": f"_:{r['order_item_id']}",
                "dgraph.type": "OrderItem",
                "order_item_id": r["order_item_id"],
                "quantity": int(r["quantity"]),
                "subtotal": float(r["subtotal"]),
                "belongs_to_order": [{
                    "uid": f"_:{r['order_id']}"
                }],

                "contains_dish": [{
                    "uid": f"_:{r['dish_id']}"
                }]
            })
    txn = client.txn()

    try:

        txn.mutate(set_obj=data)
        txn.commit()

        print("Datos cargados correctamente a Dgraph")

    finally:
        txn.discard()

