from tornado.ioloop import IOLoop
from tornado.web import Application

from modules.handlers import calculate_metrics, return_metrics
from modules.db import database

import endpoints


def app():
    urls = [(endpoints.API_CALCULATE_METRICS, calculate_metrics.CalculateMetricsHandler),
            (endpoints.API_RETURN_METRICS, return_metrics.ReturnMetricsHandler)]
    return Application(urls, debug=True)


if __name__ == "__main__":
    database.make_db()
    app().listen(4000)
    IOLoop.current().start()
