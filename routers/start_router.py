from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.psql.enums.enums import Roles
from db.psql.models import User
from middleware import MsgMiddleware, CallbackMiddleware

router = Router()

router.message.middleware(MsgMiddleware([Roles.ADMIN, Roles.STUDENT]))
router.callback_query.middleware(CallbackMiddleware([Roles.ADMIN, Roles.STUDENT]))
text = "Привет! Это бот для обучения Python. Приятного пользования!"
@router.message(CommandStart())
async def start(message: Message, user: User, state: FSMContext):
    await state.clear()
    buttons = InlineKeyboardBuilder()
    if user.roles == Roles.ADMIN:
        buttons.button(text="Управление пользователями", callback_data="admin_manage")
    buttons.button(text="Курс", callback_data="courses")
    markup = buttons.as_markup()
    await state.update_data(bt0=text)
    await state.update_data(br0=markup)
    await message.answer(text, reply_markup=markup)