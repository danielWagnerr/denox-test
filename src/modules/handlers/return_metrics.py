from typing import Optional, Awaitable
from json import dumps

import tornado.web

from modules.db import database as db


class ReturnMetricsHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        results = db.get_results()
        self.write(dumps(results))
