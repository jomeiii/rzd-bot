from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.main import main_keyboard

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"👋 Привет, {html.bold(message.from_user.full_name)}!\n\n"
        f"🚆 <b>Find Cheap Tickets Home</b>\n"
        f"Найду самые выгодные даты для поездки домой.\n\n"
        f"💰 Меньше цена — больше денег на что-нибудь приятное :)",
        reply_markup=main_keyboard
    )
    await state.clear()