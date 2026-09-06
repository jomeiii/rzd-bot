from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from bot.texts import SEARCH_TICKETS

from datetime import date, timedelta
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=SEARCH_TICKETS)
        ]
    ],
    resize_keyboard=True
)

calendar_keyboard_builder = InlineKeyboardBuilder()
today = date.today()
for i in range(9):
    current_date = today + timedelta(days=i)

    if i == 0:
        text = f"Сегодня {current_date:%d.%m}"
    elif i == 1:
        text = f"Завтра {current_date:%d.%m}"
    else:
        text = f"{current_date.strftime('%a')} {current_date:%d.%m}"

    calendar_keyboard_builder.button(
        text=text,
        callback_data=f"date:{current_date.isoformat()}"
    )
calendar_keyboard_builder.adjust(2)
calendar_keyboard = calendar_keyboard_builder.as_markup()

def train_navigation_keyboard(index: int, total: int, purchase_url: str):
    buttons = []

    if index > 0:
        buttons.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"train:{index - 1}"
            )
        )

    if index < total - 1:
        buttons.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"train:{index + 1}"
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons,
            [
                InlineKeyboardButton(
                    text="🎫 Купить билет",
                    url=purchase_url
                )
            ]
        ]
    )