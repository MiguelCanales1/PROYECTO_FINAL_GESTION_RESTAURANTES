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

