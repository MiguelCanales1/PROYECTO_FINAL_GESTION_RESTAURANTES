import json
import pydgraph
from connect import get_dgraph


# =========================================
# CONEXION
# =========================================

stub, client = get_dgraph()


# =========================================
# SCHEMA
# =========================================

schema = """

user_id: string @index(exact) .
user_name: string @index(term) .
zone: string @index(exact) .

restaurant_id: string @index(exact) .
restaurant_name: string @index(term) .
category: string @index(term) .
address: string .

dish_id: string @index(exact) .
dish_name: string @index(term) .
price: float .

order_id: string @index(exact) .
order_date: datetime @index(hour) .

driver_id: string @index(exact) .
driver_name: string @index(term) .

FAVORITE: [uid] @reverse .
PLACES: [uid] @reverse .
FROM: [uid] @reverse .
CONTAINS: [uid] @reverse .
DELIVERS: [uid] @reverse .
WORKS_IN: [uid] @reverse .
SERVES: [uid] @reverse .

type Usuario {
    user_id
    user_name
    zone
    FAVORITE
    PLACES
}

type Restaurante {
    restaurant_id
    restaurant_name
    category
    zone
    address
    SERVES
}

type Platillo {
    dish_id
    dish_name
    category
    price
}

type Pedido {
    order_id
    order_date
    FROM
    CONTAINS
}

type Repartidor {
    driver_id
    driver_name
    DELIVERS
    WORKS_IN
}

"""


def create_schema():
    operation = pydgraph.Operation(schema=schema)
    client.alter(operation)
    print("Schema cargado correctamente")


# =========================================
# 1. RESTAURANTES FAVORITOS POR USUARIO
# =========================================
def restaurantes_favoritos(user_id):
    txn = client.txn()
    query = """
    query q($user: string){
        usuarios(func: eq(user_name, $user)) {
            user_name
            FAVORITE {
                restaurant_id
                restaurant_name
                category
                zone
            }
            PLACES {
                FROM {
                    restaurant_id
                    restaurant_name
                    category
                    zone
                }
            }
        }
    }
    """
    res = txn.query(query, variables={"$user": str(user_id)})
    return json.loads(res.json)


# =========================================
# 2. PLATILLOS MÁS CONSUMIDOS
# =========================================
def platillos_usuario(user_id):
    txn = client.txn()
    query = """
    query q($user: string){
        usuarios(func: eq(user_name, $user)) {
            PLACES(first: 20) {
                FROM {
                    restaurant_id
                    restaurant_name
                }
                CONTAINS {
                    dish_id
                    dish_name
                    category
                }
            }
        }
    }
    """
    res = txn.query(query, variables={"$user": str(user_id)})
    return json.loads(res.json)


# =========================================
# 3. RESTAURANTES RELACIONADOS POR CLIENTES
# =========================================
def restaurantes_relacionados(rest_name):
    txn = client.txn()
    query = """
    query q($rest: string){
        restaurantes(func: eq(restaurant_name, $rest)) {
            restaurant_name
            ~FROM(first: 20) {
                ~PLACES {
                    user_id
                    PLACES(first: 10) {
                        FROM @filter(NOT eq(restaurant_name, $rest)) {
                            restaurant_id
                            restaurant_name
                            category
                        }
                    }
                }
            }
        }
    }
    """
    res = txn.query(query, variables={"$rest": str(rest_name)})
    return json.loads(res.json)


# =========================================
# 4. RECOMENDACION DE RESTAURANTES
# =========================================
def recomendaciones(user_id):
    txn = client.txn()
    query = """
    query q($user: string){
        usuarios(func: eq(user_name, $user)) {
            PLACES(first: 10) {
                FROM {
                    ~FROM(first: 10) {
                        ~PLACES @filter(NOT eq(user_name, $user)) {
                            user_name
                            PLACES(first: 5) {
                                FROM {
                                    restaurant_id
                                    restaurant_name
                                    category
                                    zone
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    res = txn.query(query, variables={"$user": str(user_id)})
    return json.loads(res.json)


# =========================================
# 5. USUARIOS CON PREFERENCIAS SIMILARES
# =========================================
def usuarios_similares(user_id):
    txn = client.txn()
    query = """
    query q($user: string){
        usuarios(func: eq(user_name, $user)) {
            # Relacion por restaurantes
            PLACES(first: 10) {
                FROM {
                    restaurant_name
                    ~FROM(first: 10) {
                        ~PLACES @filter(NOT eq(user_name, $user)) {
                            user_id
                            user_name
                        }
                    }
                }
                # Relacion por platillos
                CONTAINS {
                    dish_name
                    ~CONTAINS(first: 10) {
                        ~PLACES @filter(NOT eq(user_name, $user)) {
                            user_id
                            user_name
                        }
                    }
                }
            }
        }
    }
    """
    res = txn.query(query, variables={"$user": str(user_id)})
    return json.loads(res.json)


# =========================================
# 6. RESTAURANTES POR ZONA Y CATEGORIA
# =========================================
def restaurantes_zona_categoria(zona, categoria):
    txn = client.txn()
    query = """
    query q($zona: string, $categoria: string){
        restaurantes(func: eq(zone, $zona)) @filter(eq(category, $categoria)) {
            restaurant_id
            restaurant_name
            category
            zone
            address
        }
    }
    """
    res = txn.query(query, variables={"$zona": zona, "$categoria": categoria})
    return json.loads(res.json)


# =========================================
# 7. RELACION REPARTIDOR-RESTAURANTE-ZONA
# =========================================
def repartidores_restaurante(rest_name):
    txn = client.txn()
    query = """
    query q($rest: string){
        restaurantes(func: eq(restaurant_name, $rest)) {
            restaurant_id
            restaurant_name
            ~WORKS_IN {
                driver_id
                driver_name
                DELIVERS(first: 20) {
                    ~PLACES {
                        zone
                    }
                }
            }
        }
    }
    """
    res = txn.query(query, variables={"$rest": str(rest_name)})
    return json.loads(res.json)


# =========================================
# 8. RELACION COMPLETA DE PEDIDO
# =========================================
def relacion_pedido(order_id):
    txn = client.txn()
    query = """
    query q($order_id: string){
        pedidos(func: eq(order_id, $order_id)) {
            order_id
            ~PLACES {
                user_id
                user_name
            }
            FROM {
                restaurant_id
                restaurant_name
            }
            ~DELIVERS {
                driver_id
                driver_name
            }
        }
    }
    """
    res = txn.query(query, variables={"$order_id": order_id})
    return json.loads(res.json)

        