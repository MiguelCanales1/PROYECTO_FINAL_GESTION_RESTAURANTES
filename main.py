def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Consultas SQL")
        print("2. Consultas MongoDB")
        print("3. Consultas Dgraph")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_sql()
        elif opcion == "2":
            menu_mongo()
        elif opcion == "3":
            menu_dgraph()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


#  SQL
def menu_sql():
    while True:
        print("\n=== CONSULTAS SQL ===")
        print("1. Historial de pedidos por usuario")
        print("2. Pedidos recientes por usuario")
        print("3. Pedidos por restaurante")
        print("4. Pedidos por fecha")
        print("5. Pedidos por repartidor")
        print("6. Por categoría de restaurante")
        print("7. Pedidos por proveedor")
        print("8. Tipo de paquetería")
        print("0. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            print("Ejecutando consulta 1...")
        elif opcion == "2":
            print("Ejecutando consulta 2...")
        elif opcion == "3":
            print("Ejecutando consulta 3...")
        elif opcion == "4":
            print("Ejecutando consulta 4...")
        elif opcion == "5":
            print("Ejecutando consulta 5...")
        elif opcion == "6":
            print("Ejecutando consulta 6...")
        elif opcion == "7":
            print("Ejecutando consulta 7...")
        elif opcion == "8":
            print("Ejecutando consulta 8...")
        elif opcion == "0":
            break
        else:
            print("Opción inválida")


# MongoDB
def menu_mongo():
    while True:
        print("\n=== CONSULTAS MongoDB ===")
        print("9. Pedidos más costosos")
        print("10. Pedido que más tardó por usuario")
        print("11. Menú más caro")
        print("12. Pedidos más recientes por zona")
        print("13. Restaurante con más pedidos")
        print("14. Clientes con mayor gasto")
        print("15. Pedidos con mayor distancia")
        print("16. Repartidores mejor calificados")
        print("0. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "9":
            print("Ejecutando consulta 9...")
        elif opcion == "10":
            print("Ejecutando consulta 10...")
        elif opcion == "11":
            print("Ejecutando consulta 11...")
        elif opcion == "12":
            print("Ejecutando consulta 12...")
        elif opcion == "13":
            print("Ejecutando consulta 13...")
        elif opcion == "14":
            print("Ejecutando consulta 14...")
        elif opcion == "15":
            print("Ejecutando consulta 15...")
        elif opcion == "16":
            print("Ejecutando consulta 16...")
        elif opcion == "0":
            break
        else:
            print("Opción inválida")


# Dgraph 
def menu_dgraph():
    while True:
        print("\n=== CONSULTAS Dgraph ===")
        print("17. Restaurantes favoritos por usuario")
        print("18. Platillos más consumidos")
        print("19. Restaurantes relacionados")
        print("20. Recomendación de restaurantes")
        print("21. Usuarios con preferencias similares")
        print("22. Restaurantes por zona y tipo")
        print("23. Relación repartidores-restaurantes-zonas")
        print("24. Relación completa de un pedido")
        print("0. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "17":
            print("Ejecutando consulta 17...")
        elif opcion == "18":
            print("Ejecutando consulta 18...")
        elif opcion == "19":
            print("Ejecutando consulta 19...")
        elif opcion == "20":
            print("Ejecutando consulta 20...")
        elif opcion == "21":
            print("Ejecutando consulta 21...")
        elif opcion == "22":
            print("Ejecutando consulta 22...")
        elif opcion == "23":
            print("Ejecutando consulta 23...")
        elif opcion == "24":
            print("Ejecutando consulta 24...")
        elif opcion == "0":
            break
        else:
            print("Opción inválida")


# Ejecutar menu
menu_principal()