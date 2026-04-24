#!/usr/bin/env python3
import os
from cassandra.cluster import Cluster
from pymongo import MongoClient
import pydgraph

# --- CONFIG ---
CASSANDRA_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', '127.0.0.1')
DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def start_containers():
    #""" Levanta mongo y cassandra""" 
    print("Iniciando contenedores...")
    # MongoDB
    os.system("docker run -d -p 27017:27017 --name mongodb mongo 2>/dev/null || docker start mongodb")
    # Cassandra
    os.system("docker run -d -p 9042:9042 --name cassandra cassandra 2>/dev/null || docker start cassandra")

def get_cassandra():
    #""" Conexion a Cassandra """
    cluster = Cluster(CASSANDRA_IPS.split(','))
    session = cluster.connect()
    return cluster, session

def get_mongodb():
    #""" Conexion a MongoDB """
    client = MongoClient('mongodb://localhost:27017/')
    db = client["restaurante_db"]
    coll = db["pedidos_detalles"] 
    return client, db, coll

def get_dgraph():
    #""" Conexion a Dgraph """
    stub = pydgraph.DgraphClientStub(DGRAPH_URI)
    client = pydgraph.DgraphClient(stub)
    return stub, client