from typing import Any
from datetime import datetime

from config import DATETIME_FORMAT


def send_error(handler: Any, status_code: int, message: str = "") -> None:
    handler.clear()
    handler.set_status(status_code)
    handler.finish(message)


def get_calculate_metrics_data(data: dict) -> tuple:
    assert data.get('serial') is not None and data.get('datahora_inicio') is not None and \
            data.get('datahora_fim') is not None, "Há atributos faltantes em seu payload, por favor, me envie os " \
                                                  "dados de acordo com a documentação"

    serial = str(data['serial'])
    initial_timestamp = int(datetime.strptime(data['datahora_inicio'], DATETIME_FORMAT).timestamp())
    final_timestamp = int(datetime.strptime(data['datahora_fim'], DATETIME_FORMAT).timestamp())

    return serial, initial_timestamp, final_timestamp
