from connect import get_cassandra
from connect import get_mongodb
from connect import get_dgraph
from connect import start_containers

start_containers()

stub, client_dg = get_dgraph
client, db_mongo, coll = get_mongodb()
cluster, session = get_cassandra()
session.set_keyspace("restaurante_db")

def mostrar_pedido(row):

    print("\n================================")

    if hasattr(row, 'id_pedido'):
        print(f"Pedido: {row.id_pedido}")

    if hasattr(row, 'usuario'):
        print(f"Usuario: {row.usuario}")

    if hasattr(row, 'restaurante'):
        print(f"Restaurante: {row.restaurante}")

    if hasattr(row, 'repartidor'):
        print(f"Repartidor: {row.repartidor}")

    if hasattr(row, 'estado'):
        print(f"\nEstado: {row.estado}")

    if hasattr(row, 'total'):
        print(f"Total: ${row.total}")

    if hasattr(row, 'distancia'):
        print(f"\nDistancia: {row.distancia} km")

    if hasattr(row, 'tiempo_entrega'):
        print(f"Tiempo entrega: {row.tiempo_entrega} min")

    if hasattr(row, 'calificacion'):
        print(f"Calificación: {row.calificacion}")

    if hasattr(row, 'fecha'):
        print(f"\nFecha: {row.fecha}")

    print("================================")

def mostrar_menu():
    print("\n========== GESTION DE RESTAURANTES ==========")

    print("\n--------------- CONSULTAS ----------------")

    # CASSANDRA
    print("\n[CASSANDRA]")
    print("1. Historial de pedidos por usuario")
    print("2. Ultimos pedidos entregados de un usuario")
    print("3. Pedidos por restaurante")
    print("4. Pedidos por fecha")
    print("5. Pedidos por repartidor")
    print("6. Pedidos por zona y restaurante")
    print("7. Entregas por paqueteria")
    print("8. Ver pedidos recientes")

    # MONGODB
    print("\n[MONGODB]")
    print("9. Pedidos mas costosos por cliente")
    print("10. Pedido que mas tardo en llegar")
    print("11. Clientes mas frecuentes de restaurante")
    print("12. Pedidos recientes por codigo postal")
    print("13. Restaurantes con mas pedidos")
    print("14. Clientes con mayor gasto total")
    print("15. Pedidos con mayor distancia")
    print("16. Mejores repartidores")

    # DGRAPH
    print("\n[DGRAPH]")
    print("17. Restaurantes favoritos por usuario")
    print("18. Platillos mas consumidos")
    print("19. Restaurantes relacionados")
    print("20. Recomendacion de restaurantes")
    print("21. Usuarios con preferencias similares")
    print("22. Restaurantes por zona y categoria")
    print("23. Relacion repartidor-restaurante-zona")
    print("24. Relacion completa de pedido")

    print("\n0. Salir")

while True:

    mostrar_menu()

    opcion = input("\nSelecciona una opcion: ")

    if opcion == "0":
        print("\nSaliendo del sistema...")
        break

    elif opcion == "1":
        usuario = input("Nombre del usuario: ")

        query = """
        SELECT * FROM pedidos_por_usuario
        WHERE usuario = %s;
        """

        rows = session.execute(query, [usuario])

        print("\n--- HISTORIAL DE PEDIDOS ---")
        for row in rows:
             mostrar_pedido(row)

    elif opcion == "2":
        usuario = input("Nombre del usuario: ")

        query = """
        SELECT * FROM pedidos_por_usuario
        WHERE usuario = %s
        LIMIT 10;
        """

        rows = session.execute(query, [usuario])

        print("\n--- ULTIMOS PEDIDOS ENTREGADOS ---")
        for row in rows:
            if row.estado == "entregado":
                 mostrar_pedido(row)

    elif opcion == "3":
        restaurante = input("Nombre del restaurante: ")

        query = """
        SELECT * FROM pedidos_por_restaurante
        WHERE restaurante = %s;
        """

        rows = session.execute(query, [restaurante])

        print("\n--- PEDIDOS DEL RESTAURANTE ---")
        for row in rows:
             mostrar_pedido(row)

    elif opcion == "4":
        fecha = input("Fecha (YYYY-MM-DD): ")

        query = """
        SELECT * FROM pedidos_por_fecha
        WHERE fecha = %s;
        """

        rows = session.execute(query, [fecha])

        print("\n--- PEDIDOS POR FECHA ---")
        for row in rows:
             mostrar_pedido(row)

    elif opcion == "5":
        repartidor = input("Nombre del repartidor: ")

        query = """
        SELECT * FROM pedidos_por_repartidor
        WHERE repartidor = %s;
        """

        rows = session.execute(query, [repartidor])

        print("\n--- PEDIDOS DEL REPARTIDOR ---")
        for row in rows:
             mostrar_pedido(row)

    elif opcion == "6":
        zona = input("Zona: ")
        restaurante = input("Restaurante: ")

        query = """
        SELECT * FROM pedidos_por_zona_restaurante
        WHERE zona = %s
        AND restaurante = %s;
        """

        rows = session.execute(query, [zona, restaurante])

        print("\n--- PEDIDOS POR ZONA Y RESTAURANTE ---")
        for row in rows:
             mostrar_pedido(row)

    elif opcion == "7":
        paqueteria = input("Tipo de paqueteria: ")

        query = """
        SELECT * FROM entregas_por_paqueteria
        WHERE tipo_paqueteria = %s;
        """

        rows = session.execute(query, [paqueteria])

        print("\n--- ENTREGAS POR PAQUETERIA ---")
        for row in rows:
             mostrar_pedido(row)

    elif opcion == "8":
        query = """
        SELECT * FROM pedidos_por_usuario
        LIMIT 20;
        """

        rows = session.execute(query)

        print("\n--- PEDIDOS RECIENTES ---")
        for row in rows:
             mostrar_pedido(row)
    #------------------
    #MongoDB
    #-----------------
    elif opcion == "9":
        print("\nPedidos mas costosos por cliente")
        pipeline = [
            {"$group": {"_id": "$customerName", "maxGasto": {"$max": "$orderPrice"}}},
            {"$sort": {"maxGasto": -1}}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"Cliente: {res['_id']} y su pedido mas caro es de ${res['maxGasto']}")

    elif opcion == "10":
        print("\nPedido que mas tardo y menor distancia por cliente")
        pipeline = [
            {"$group": {
                "_id": "$customerName", 
                "PedidoConMayorTardanza": {"$max": "$deliveryTime"},
                "PedidoConMenorDistancia": {"$min": "$deliveryDistance"}
            }}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"Cliente: {res['_id']}, tiempo maximo de entrega: {res['PedidoConMayorTardanza']}, pedido con la distancia mas corta: {res['PedidoConMenorDistancia']} km")

    elif opcion == "11":
        rest_name = input("Nombre del restaurante")
        print(f"\nTop clientes de {rest_name}")
        pipeline = [
            {"$match": {"restaurantName": rest_name}}, 
            {"$group": {"_id": "$customerName", "CantidadTotalDePedidosAlRestaurante": {"$count": {}}}},
            {"$sort": {"CantidadTotalDePedidosAlRestaurante": -1 }},
            {"$limit": 10}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"Cliente: {res['_id']} tiene {res['CantidadTotalDePedidosAlRestaurante']} pedidos")

    elif opcion == "12":
        colonia = input("Introduce el nombre de la colonia")
        print(f"\nUltimos pedidos en {colonia}")
        pipeline = [
            {"$match": {"postCode": colonia}}, 
            {"$sort": {"orderDate" : -1}}, 
            {"$limit": 5},
            {"$project": {"_id": 0, "customerName": 1, "orderDate": 1, "restaurantName": 1}}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(res)

    elif opcion == "13":
        print("\nTop restaurantes con mayor cantidad de pedidos")
        pipeline = [
            {"$group": {"_id": "$restaurantName", "TotalPedidos": {"$count": {}}}}, 
            {"$sort": {"TotalPedidos": -1}}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"Restaurante: {res['_id']} tiene {res['TotalPedidos']} pedidos")

    elif opcion == "14":
        print("\nClientes con mayor gasto total")
        pipeline = [
            {"$group": {"_id": "$customerName", "GastoTotal": {"$sum": "$orderPrice" }, "TotalOrdenes": {"$count": {}}}},
            {"$sort": {"GastoTotal": -1}}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"Cliente: {res['_id']} gasto en total: ${res['GastoTotal']:.2f} y sus ordenes en total son: {res['TotalOrdenes']}")

    elif opcion == "15":
        print("\nTop pedidos con la mayor distancia")
        pipeline = [
            {"$match": {"deliveryDistance": {"$gte": 10}}},
            {"$sort": {"deliveryDistance": -1}},
            {"$limit": 10} 
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"ID de la orden: {res['orderID']} distancia de entrega {res['deliveryDistance']} km del cliente {res['customerName']}")

    elif opcion == "16":
        print("\nTop repartidores")
        pipeline = [
            {"$group": {"_id": "$delivererName", "Rating": {"$avg": "$deliveryRating" }}},
            {"$sort": {"Rating":-1}}, 
            {"$limit": 5}
        ]
        results = coll.aggregate(pipeline)
        for res in results:
            print(f"Repartidor: {res['_id']} su rating es {res['Rating']:.2f}")
    

    # --- DGRAPH (con prefijo dg.) ---
    elif opcion == "17":
        user_id = input("Nombre del usuario: ")
        res = dg.restaurantes_favoritos(user_id)
        print(f"\n--- RESTAURANTES DE {user_id.upper()} ---")
        seen = set()
        for u in res.get("usuarios", []):
            for f in u.get("FAVORITE", []):
                rid = f['restaurant_id']
                if rid not in seen:
                    print(f"- {f['restaurant_name']} ({f['category']}) en {f['zone']} [Favorito]")
                    seen.add(rid)
            for p in u.get("PLACES", []):
                for f in p.get("FROM", []):
                    rid = f['restaurant_id']
                    if rid not in seen:
                        print(f"- {f['restaurant_name']} ({f['category']}) en {f['zone']} [Frecuente]")
                        seen.add(rid)

    elif opcion == "18":
        user_id = input("Nombre del usuario: ")
        res = dg.platillos_usuario(user_id)
        print(f"\n--- PLATILLOS DE {user_id.upper()} ---")
        for u in res.get("usuarios", []):
            for p in u.get("PLACES", []):
                rest = p.get("FROM", [{}])[0]
                for dish in p.get("CONTAINS", []):
                    print(f"- {dish['dish_name']} ({dish['category']}) en {rest.get('restaurant_name')}")

    elif opcion == "19":
        rest_name = input("Nombre del restaurante: ")
        res = dg.restaurantes_relacionados(rest_name)
        print(f"\n--- RELACIONADOS CON {rest_name.upper()} ---")
        related = {}
        for r in res.get("restaurantes", []):
            for order in r.get("~FROM", []):
                for user in order.get("~PLACES", []):
                    for u_order in user.get("PLACES", []):
                        for other_rest in u_order.get("FROM", []):
                            rid = other_rest['restaurant_id']
                            if rid not in related:
                                related[rid] = {"name": other_rest['restaurant_name'], "cat": other_rest['category'], "count": 0}
                            related[rid]["count"] += 1
        for rid, data in related.items():
            print(f"- {data['name']} ({data['cat']}) | Clientes en común: {data['count']}")

    elif opcion == "20":
        user_id = input("Nombre del usuario: ")
        res = dg.recomendaciones(user_id)
        print(f"\n--- RECOMENDACIONES PARA {user_id.upper()} ---")
        seen = set()
        for u in res.get("usuarios", []):
            for p in u.get("PLACES", []):
                for f in p.get("FROM", []):
                    for fr in f.get("~FROM", []):
                        for u_sim in fr.get("~PLACES", []):
                            for p_sim in u_sim.get("PLACES", []):
                                for r_rec in p_sim.get("FROM", []):
                                    rid = r_rec['restaurant_id']
                                    if rid not in seen:
                                        print(f"- {r_rec['restaurant_name']} ({r_rec['category']}) en {r_rec['zone']} | Razón: Gustos similares")
                                        seen.add(rid)

    elif opcion == "21":
        user_id = input("Nombre del usuario: ")
        res = dg.usuarios_similares(user_id)
        print(f"\n--- USUARIOS SIMILARES A {user_id.upper()} ---")
        sim_users = {}
        for u in res.get("usuarios", []):
            for p in u.get("PLACES", []):
                for r in p.get("FROM", []):
                    for order in r.get("~FROM", []):
                        for other_u in order.get("~PLACES", []):
                            name = other_u['user_name']
                            if name not in sim_users: sim_users[name] = {"id": other_u['user_id'], "rest": set(), "dish": set()}
                            sim_users[name]["rest"].add(r['restaurant_name'])
                for d in p.get("CONTAINS", []):
                    for d_order in d.get("~CONTAINS", []):
                        for other_u in d_order.get("~PLACES", []):
                            name = other_u['user_name']
                            if name not in sim_users: sim_users[name] = {"id": other_u['user_id'], "rest": set(), "dish": set()}
                            sim_users[name]["dish"].add(d['dish_name'])
        for name, data in sim_users.items():
            if name != user_id:
                print(f"- {name} (ID: {data['id']}) | Rest. común: {len(data['rest'])}, Platillos común: {len(data['dish'])}")

    elif opcion == "22":
        zona = input("Zona: ")
        cat = input("Categoría: ")
        res = dg.restaurantes_zona_categoria(zona, cat)
        print(f"\n--- RESTAURANTES EN {zona} ({cat}) ---")
        for r in res.get("restaurantes", []):
            print(f"- {r['restaurant_name']} en {r['address']} (ID: {r['restaurant_id']})")

    elif opcion == "23":
        rest_name = input("Nombre del restaurante: ")
        res = dg.repartidores_restaurante(rest_name)
        print(f"\n--- REPARTIDORES PARA {rest_name.upper()} ---")
        seen_drivers = set()
        for r in res.get("restaurantes", []):
            for w in r.get("~WORKS_IN", []):
                driver_id = w.get('driver_id')
                if driver_id not in seen_drivers:
                    zones = set()
                    for delivery in w.get("DELIVERS", []):
                        for user in delivery.get("~PLACES", []):
                            zones.add(user.get("zone", "N/A"))
                    print(f"- {w['driver_name']} | Zonas: {', '.join(zones)}")
                    seen_drivers.add(driver_id)

    elif opcion == "24":
        order_id = input("ID del pedido: ").strip()
        if order_id:
            res = dg.relacion_pedido(order_id)
            print(f"\n--- DETALLE DEL PEDIDO {order_id} ---")
            for p in res.get("pedidos", []):
                user = p.get("~PLACES", [{}])[0]
                rest = p.get("FROM", [{}])[0]
                driver = p.get("~DELIVERS", [{}])[0]
                print(f"- Cliente: {user.get('user_name', 'N/A')}")
                print(f"- Restaurante: {rest.get('restaurant_name', 'N/A')}")
                print(f"- Repartidor: {driver.get('driver_name', 'N/A')}")
  
    else:
        print("\nOpcion invalida.")

cluster.shutdown()
cluster.shutdown()
