from connect import get_cassandra

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

    elif opcion == "9":
        print("\nConsulta MongoDB 1")

    elif opcion == "10":
        print("\nConsulta MongoDB 2")

    elif opcion == "11":
        print("\nConsulta MongoDB 3")

    elif opcion == "12":
        print("\nConsulta MongoDB 4")

    elif opcion == "13":
        print("\nConsulta MongoDB 5")

    elif opcion == "14":
        print("\nConsulta MongoDB 6")

    elif opcion == "15":
        print("\nConsulta MongoDB 7")

    elif opcion == "16":
        print("\nConsulta MongoDB 8")
    
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