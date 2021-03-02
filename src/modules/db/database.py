from typing import Type
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection

import endpoints
from config import TRACKING_COLLECTION, RESULTS_COLLECTION

client: Type[MongoClient]


def make_db() -> None:
    global client
    client = MongoClient(host=endpoints.DB_HOST, port=endpoints.DB_PORT)


def get_travels(serial: str, initial_timestamp: int, final_timestamp: int) -> list:
    global client
    tracking_collection: Collection = client.denox[TRACKING_COLLECTION]

    query = {'serial': serial, 'datahora': {"$gte": initial_timestamp, "$lte": final_timestamp}}
    response = tracking_collection.find(query).sort("datahora", ASCENDING)
    return response


def insert_results(result: dict) -> None:
    global client
    results_collection: Collection = client.denox[RESULTS_COLLECTION]
    results_collection.insert_one(dict(result))


def get_results() -> list:
    global client
    results_collection: Collection = client.denox[RESULTS_COLLECTION]
    response = results_collection.find({}, {'_id': False})
    return list(response)
