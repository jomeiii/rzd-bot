from datetime import date, timedelta

import rzd_api.exceptions
from rzd_api import RzdClient


def search_tickets(from_station: str | int, to_station: str | int, departure_date: date) -> int:
    with RzdClient() as client:
        try:
            trains = client.search_tickets(
                from_station=from_station,
                to_station=to_station,
                departure_date=departure_date
            )

            for train in trains:
                print(f"Поезд: {train.number}")
                print(f"Откуда: {train.origin_name}")
                print(f"Куда: {train.destination_name}")
                print(f"Отправление: {train.departure_time}")
                print(f"Прибытие: {train.arrival_time}")
                print(f"Цена от: {train.min_price} ₽")
                print(f"Мест: {train.available_places}")
                print()

                return 0

        except rzd_api.exceptions.RzdAPIError as e:
            if e.code == 310:
                print('Поездов нет в этот день')
                return 310
