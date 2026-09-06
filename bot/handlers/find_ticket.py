from datetime import datetime

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.main import calendar_keyboard
from bot.states.search import SearchState
from bot.texts import SEARCH_TICKETS

from rzd.client import search_tickets

router = Router()

from_city = ''
to_city = ''

@router.message(F.text == SEARCH_TICKETS)
async def search_ticket(message: Message, state: FSMContext):
    await message.answer("Введите, откуда вы едете",
                         reply_markup=None)
    await state.set_state(SearchState.waiting_from)
@router.message(SearchState.waiting_from)
async def get_from_city(message: Message, state: FSMContext):
    global from_city
    from_city = message.text
    await message.answer('Введите, куда вы едете')
    await state.set_state(SearchState.waiting_to)

@router.message(SearchState.waiting_to)
async def get_to_city(message: Message, state: FSMContext):
    global to_city
    to_city = message.text
    await message.answer('Выберите дату',
                         reply_markup=calendar_keyboard)
    await state.clear()

@router.callback_query(F.data.startswith("date:"))
async def select_date(callback: CallbackQuery):
    selected_date = callback.data.split(":")[1].split('-')
    years = selected_date[0]
    mounts = selected_date[1]
    days = selected_date[2]
    departure_date = datetime(int(years), int(mounts), int(days))
    trains = search_tickets(from_station=from_city,
                   to_station=to_city,
                   departure_date=departure_date)

    if trains is None:
        await callback.message.answer(f'Поездов в этот день нет.')
    else:
        train = trains[0]
        departure = datetime.fromisoformat(train.departure_time)
        arrival = datetime.fromisoformat(train.arrival_time)
        await callback.message.answer(
            f"🚆 <b>Найдено {len(trains)} поездов</b>\n\n"
            f"🛤 <b>Маршрут</b>\n"
            f"{html.bold(train.origin_name)} → {html.bold(train.destination_name)}\n\n"
            f"🕐 <b>Отправление:</b> {departure:%d.%m.%Y в %H:%M}\n"
            f"🏁 <b>Прибытие:</b> {arrival:%d.%m.%Y в %H:%M}\n"
            f"💰 <b>Цена от:</b> {train.min_price:.0f} ₽\n"
            f"💺 <b>Свободных мест:</b> {train.available_places}\n\n"
            f"🚂 <b>Поезд:</b> {train.number}",
        )