from connect import get_cassandra
from connect import get_mongodb

client, db_mongo, coll = get_mongodb()
cluster, session = get_cassandra()
session.set_keyspace("restaurante_db")

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
            print(row)

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
                print(row)

    elif opcion == "3":
        restaurante = input("Nombre del restaurante: ")

        query = """
        SELECT * FROM pedidos_por_restaurante
        WHERE restaurante = %s;
        """

        rows = session.execute(query, [restaurante])

        print("\n--- PEDIDOS DEL RESTAURANTE ---")
        for row in rows:
            print(row)

    elif opcion == "4":
        fecha = input("Fecha (YYYY-MM-DD): ")

        query = """
        SELECT * FROM pedidos_por_fecha
        WHERE fecha = %s;
        """

        rows = session.execute(query, [fecha])

        print("\n--- PEDIDOS POR FECHA ---")
        for row in rows:
            print(row)

    elif opcion == "5":
        repartidor = input("Nombre del repartidor: ")

        query = """
        SELECT * FROM pedidos_por_repartidor
        WHERE repartidor = %s;
        """

        rows = session.execute(query, [repartidor])

        print("\n--- PEDIDOS DEL REPARTIDOR ---")
        for row in rows:
            print(row)

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
            print(row)

    elif opcion == "7":
        paqueteria = input("Tipo de paqueteria: ")

        query = """
        SELECT * FROM entregas_por_paqueteria
        WHERE tipo_paqueteria = %s;
        """

        rows = session.execute(query, [paqueteria])

        print("\n--- ENTREGAS POR PAQUETERIA ---")
        for row in rows:
            print(row)

    elif opcion == "8":
        query = """
        SELECT * FROM pedidos_por_usuario
        LIMIT 20;
        """

        rows = session.execute(query)

        print("\n--- PEDIDOS RECIENTES ---")
        for row in rows:
            print(row)
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
    
    elif opcion == "17":
        print("\nConsulta Dgraph 1")

    elif opcion == "18":
        print("\nConsulta Dgraph 2")

    elif opcion == "19":
        print("\nConsulta Dgraph 3")

    elif opcion == "20":
        print("\nConsulta Dgraph 4")

    elif opcion == "21":
        print("\nConsulta Dgraph 5")

    elif opcion == "22":
        print("\nConsulta Dgraph 6")

    elif opcion == "23":
        print("\nConsulta Dgraph 7")

    elif opcion == "24":
        print("\nConsulta Dgraph 8")
    
    else:
        print("\nOpcion invalida.")

cluster.shutdown()
cluster.shutdown()
