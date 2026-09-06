from datetime import datetime

from urllib.parse import urlencode

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from rzd_api import TrainRoute

from bot.keyboards.main import calendar_keyboard, train_navigation_keyboard
from bot.states.search import SearchState
from bot.texts import SEARCH_TICKETS

from rzd.client import search_tickets

router = Router()


@router.message(F.text == SEARCH_TICKETS)
async def search_ticket(message: Message, state: FSMContext):
    await message.answer(
        "Введите, откуда вы едете",
        reply_markup=None
    )
    await state.set_state(SearchState.waiting_from)


@router.message(SearchState.waiting_from)
async def get_from_city(message: Message, state: FSMContext):
    await state.update_data(from_city=message.text)

    await message.answer("Введите, куда вы едете")
    await state.set_state(SearchState.waiting_to)


@router.message(SearchState.waiting_to)
async def get_to_city(message: Message, state: FSMContext):
    await state.update_data(to_city=message.text)

    await message.answer(
        "Выберите дату",
        reply_markup=calendar_keyboard
    )
    await state.set_state(SearchState.waiting_date)


@router.callback_query(SearchState.waiting_date, F.data.startswith("date:"))
async def select_date(callback: CallbackQuery, state: FSMContext):
    departure_date = datetime.fromisoformat(
        callback.data.split(":")[1]
    )

    data = await state.get_data()
    from_station = data["from_city"]
    to_station = data["to_city"]

    await state.update_data(departure_date=departure_date)

    trains = search_tickets(
        from_station=from_station,
        to_station=to_station,
        departure_date=departure_date
    )

    if not trains:
        await callback.message.answer("Поездов в этот день нет.")
        await callback.answer()
        return

    await state.update_data(trains=trains)

    await callback.message.edit_text(
        get_train_info(trains, 0),
        reply_markup=train_navigation_keyboard(0, len(trains), get_tutu_purchase_link(trains[0])))

    await state.set_state(SearchState.viewing_trains)
    await callback.answer()


@router.callback_query(F.data.startswith("train:"), SearchState.viewing_trains)
async def change_train(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])

    data = await state.get_data()
    trains = data["trains"]

    await callback.message.edit_text(
        get_train_info(trains, index),
        reply_markup=train_navigation_keyboard(index, len(trains), get_tutu_purchase_link(trains[index]))
    )

    await callback.answer()


def get_train_info(trains: TrainRoute, index: int) -> str:
    train = trains[index]

    departure = datetime.fromisoformat(train.raw["LocalDepartureDateTime"])
    arrival = datetime.fromisoformat(train.raw["LocalArrivalDateTime"])

    return (
        f"🚆 <b>Поезд {index + 1} из {len(trains)}</b>\n\n"
        f"🛤 <b>Маршрут</b>\n"
        f"{html.bold(train.origin_name)} → {html.bold(train.destination_name)}\n\n"
        f"🕐 <b>Отправление:</b> {departure:%d.%m.%Y в %H:%M}\n"
        f"🏁 <b>Прибытие:</b> {arrival:%d.%m.%Y в %H:%M}\n"
        f"💰 <b>Цена от:</b> {train.min_price:.0f} ₽\n"
        f"💺 <b>Свободных мест:</b> {train.available_places}\n\n"
        f"🚂 <b>Поезд:</b> {train.number}"
    )


def get_tutu_purchase_link(train: TrainRoute) -> str:
    params = {
        "departure_st": train.origin_code,
        "arrival_st": train.destination_code,
        "dep_st": train.origin_code,
        "arr_st": train.destination_code,
        "tn": train.number,
        "date": datetime.fromisoformat(
            train.raw["LocalDepartureDateTime"]
        ).strftime("%d.%m.%Y %H:%M:%S"),
    }

    return "https://www.tutu.ru/poezda/order/?" + urlencode(params)
