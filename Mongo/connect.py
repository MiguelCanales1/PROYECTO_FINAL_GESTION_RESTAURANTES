from pymongo import MongoClient

def get_mongodb():
    """Conexión a MongoDB (Docker)"""
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["restaurante_db"] 
        coll = db["pedidos"]  
        return client, db, coll
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        return None, None, None

def get_cassandra():
    """Conexión a Cassandra (Docker)"""
    try:
        # Cambia '127.0.0.1' por la IP de tu contenedor si es necesario
        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect()
        return cluster, session
    except Exception as e:
        print(f"Error conectando a Cassandra: {e}")
        return None, None

# Si vas a usar DGraph más adelante, puedes agregar su conexión aquí