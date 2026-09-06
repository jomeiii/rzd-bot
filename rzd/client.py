from datetime import date, timedelta

import rzd_api.exceptions
from rzd_api import RzdClient, TrainRoute


def search_tickets(from_station: str | int, to_station: str | int, departure_date: date) -> list[TrainRoute] | None:
    with RzdClient() as client:
        try:
            trains = client.search_tickets(
                from_station=from_station,
                to_station=to_station,
                departure_date=departure_date
            )
            return trains

        except rzd_api.exceptions.RzdAPIError as e:
            if e.code == 310:
                return None

