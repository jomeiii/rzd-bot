from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=" 🚂 Найти билеты")
        ]
    ],
    resize_keyboard=True
)
