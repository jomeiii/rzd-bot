from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import date, timedelta
from bot.texts import SEARCH_TICKETS


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=SEARCH_TICKETS)
        ]
    ],
    resize_keyboard=True
)

calendar_keyboard_builder = InlineKeyboardBuilder()
for i in range(9):
    date = date.today() + timedelta(days=i)
    calendar_keyboard_builder.button(
        text=date.isoformat(),
        callback_data=f"date:{date.isoformat()}"
    )

calendar_keyboard_builder.adjust(3)
calendar_keyboard = calendar_keyboard_builder.as_markup()