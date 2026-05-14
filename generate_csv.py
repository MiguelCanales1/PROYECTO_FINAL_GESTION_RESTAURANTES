import csv
import uuid
import random
from faker import Faker

fake = Faker("es_MX")

# =========================================
# DATOS BASE
# =========================================

usuarios = [
    "Miguel",
    "Ana",
    "Carlos",
    "Fernanda",
    "Luis",
    "Sofia",
    "Diego",
    "Valeria"
]

restaurantes = [
    ("Tacos MX", "Mexicana"),
    ("Pizza Planet", "Italiana"),
    ("Sushi Roll", "Japonesa"),
    ("Burger House", "Americana"),
    ("Pasta Italia", "Italiana"),
    ("Wok Express", "China")
]

repartidores = [
    "Juan Perez",
    "Carlos Lopez",
    "Mario Ruiz",
    "Pedro Sanchez"
]

paqueterias = [
    "Uber Eats",
    "Didi Food",
    "Rappi"
]

estados = [
    "entregado",
    "pendiente",
    "cancelado"
]

metodos_pago = [
    "Tarjeta",
    "Efectivo"
]

zonas = [
    "Centro",
    "Americana",
    "Zapopan",
    "Providencia",
    "Chapultepec"
]

# =========================================
# CREAR CSV
# =========================================

with open("data/pedidos.csv", mode="w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    # ENCABEZADOS
    writer.writerow([
        "usuario",
        "fecha",
        "id_pedido",
        "restaurante",
        "categoria_restaurante",
        "total",
        "estado",
        "repartidor",
        "tiempo_entrega",
        "distancia",
        "calificacion",
        "metodo_pago",
        "zona",
        "direccion",
        "tipo_paqueteria"
    ])

    # GENERAR 300 PEDIDOS
    for _ in range(300):

        restaurante, categoria = random.choice(restaurantes)

        writer.writerow([
            random.choice(usuarios),
            fake.date_time_this_year(),
            str(uuid.uuid4()),
            restaurante,
            categoria,
            round(random.uniform(80, 700), 2),
            random.choice(estados),
            random.choice(repartidores),
            random.randint(15, 90),
            round(random.uniform(1, 20), 2),
            random.randint(1, 5),
            random.choice(metodos_pago),
            random.choice(zonas),
            fake.address().replace("\n", " "),
            random.choice(paqueterias)
        ])

print("CSV generado correctamente.")