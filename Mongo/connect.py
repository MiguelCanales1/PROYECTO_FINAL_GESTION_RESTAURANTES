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