import os
import logging
from dotenv import load_dotenv
from neo4j import GraphDatabase

logging.getLogger("neo4j").setLevel(logging.CRITICAL)
load_dotenv()

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        _driver = GraphDatabase.driver(uri, auth=(user, password))
    return _driver

_warned_once = False

def run_query(query, parameters=None):
    global _warned_once
    try:
        driver = get_driver()
        with driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    except Exception as e:
        if not _warned_once:
            print(f"[neo4j_client] Neo4j appears unreachable, skipping graph updates for this run: {e}")
            _warned_once = True
        return []