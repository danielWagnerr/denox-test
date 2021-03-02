from typing import Optional, Awaitable
from json import loads
import itertools
from math import radians, cos, sin, asin, sqrt

import tornado.web
import numpy as np
from sklearn.cluster import KMeans

from modules.handlers import handle_helper
from modules.db import database as db


class CalculateMetricsHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        body = loads(self.request.body)

        try:
            serial, initial_timestamp, final_timestamp = handle_helper.get_calculate_metrics_data(body)
        except (AssertionError, ValueError) as e:
            return handle_helper.send_error(self, 400, str(e))

        travels = list(db.get_travels(serial, initial_timestamp, final_timestamp))

        pairwise_travels = self.__pairwise(travels)
        total_distance = self.__get_total_distance(pairwise_travels)
        stopped_time = self.__get_stopped_time(pairwise_travels)
        moving_time = self.__get_moving_time(pairwise_travels)
        stopped_positions = self.__get_stopped_positions(travels)
        centroids = self.__get_centroids(stopped_positions)

        result = {
            "serial": serial,
            "distancia_percorrida": total_distance,
            "tempo_parado": stopped_time,
            "tempo_em_movimento": moving_time,
            "centroides_paradas": centroids
        }

        db.insert_results(result)
        self.write(result)

    def __get_total_distance(self, pairwise_travels: list) -> float:
        total_distance = 0
        for p in pairwise_travels:
            travel1, travel2 = p

            distance = self.__get_distance(travel1['longitude'], travel1['latitude'],
                                           travel2['longitude'], travel2['latitude'])
            total_distance += distance

        return round(total_distance, 3)

    @staticmethod
    def __get_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return km

    @staticmethod
    def __pairwise(iterable: list) -> list:
        a, b = itertools.tee(iterable)
        next(b, None)
        return list(zip(a, b))

    @staticmethod
    def __get_stopped_time(pairwise_travels: list) -> float:
        stopped_time = 0
        for p in pairwise_travels:
            travel1, travel2 = p
            if not travel1['situacao_movimento']:
                stopped_time += (travel2['datahora'] - travel1['datahora'])

        return stopped_time

    @staticmethod
    def __get_moving_time(pairwise_travels: list):
        moving_time = 0
        for p in pairwise_travels:
            travel1, travel2 = p
            if travel1['situacao_movimento']:
                moving_time += (travel2['datahora'] - travel1['datahora'])

        return moving_time

    @staticmethod
    def __get_stopped_positions(travels: list) -> np.ndarray:
        stopped_positions = []

        last_lat = 0
        last_long = 0

        for t in travels:
            if not t['situacao_movimento']:
                current_lat = t['latitude']
                current_long = t['longitude']

                if last_lat != current_lat and last_long != current_long:
                    last_lat = current_lat
                    last_long = current_long

                    stopped_positions.append([current_lat, current_long])

        return np.array(stopped_positions)

    @staticmethod
    def __get_centroids(stopped_positions):
        if len(stopped_positions) == 0:
            return []

        kmeans = KMeans(n_clusters=len(stopped_positions))
        kmeans.fit_predict(stopped_positions)

        return kmeans.cluster_centers_.tolist()
