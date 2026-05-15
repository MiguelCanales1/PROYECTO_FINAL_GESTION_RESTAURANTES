#!/usr/bin/env python3
import os
from cassandra.cluster import Cluster
from pymongo import MongoClient
import pydgraph

# --- CONFIG ---
CASSANDRA_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', '127.0.0.1')
DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def start_containers():
    #""" Levanta mongo, cassandra y dgraph """ 
    print("Iniciando contenedores (Docker)...")

    # MongoDB
    os.system("docker run -d -p 27017:27017 --name mongodb mongo 2>nul || docker start mongodb")
    # Cassandra
    os.system("docker run -d -p 9042:9042 --name cassandra cassandra 2>nul || docker start cassandra")
    # Dgraph
    os.system("docker run -d -p 8080:8080 -p 9080:9080 --name dgraph dgraph/standalone:latest 2>nul || docker start dgraph")

def get_cassandra():
    #""" Conexion a Cassandra """
    cluster = Cluster(CASSANDRA_IPS.split(','))
    session = cluster.connect()
    return cluster, session
    



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

def get_dgraph():

    #""" Conexion a Dgraph """
    stub = pydgraph.DgraphClientStub(DGRAPH_URI)
    client = pydgraph.DgraphClient(stub)
    return stub, client