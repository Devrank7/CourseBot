from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from db.psql.enums.enums import Roles
from middleware import MsgMiddleware, CallbackMiddleware
from routers.course_modules_router import module1_router, module3_router, module2_router

router = Router()
router.include_router(module1_router.router)
router.include_router(module2_router.router)
router.include_router(module3_router.router)
router.message.middleware(MsgMiddleware([Roles.ADMIN, Roles.STUDENT]))
router.callback_query.middleware(CallbackMiddleware([Roles.ADMIN, Roles.STUDENT]))


def course_module_markup(with_back: bool = True):
    buttons = [
        [InlineKeyboardButton(text="Модуль 1", callback_data="module_1")],
        [InlineKeyboardButton(text="Модуль 2", callback_data="module_2")],
        [InlineKeyboardButton(text="Модуль 3", callback_data="module_3")],
    ]
    if with_back:
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_0")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("course"))
async def course(message: Message, state: FSMContext):
    markup = course_module_markup(False)
    text = "Здесь будет имя курса"
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await message.answer(text, reply_markup=markup)

@router.callback_query(F.data == "courses")
async def course(query: CallbackQuery, state: FSMContext):
    markup = course_module_markup()
    text = "Здесь будет имя курса"
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await (query.message.edit_text(text, reply_markup=markup))