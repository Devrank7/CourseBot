from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from middleware import MsgMiddleware, CallbackMiddleware
from routers.admin_routers import add_user_router, delete_user_router

router = Router()
router.include_router(add_user_router.router)
router.include_router(delete_user_router.router)
router.message.middleware(MsgMiddleware())
router.callback_query.middleware(CallbackMiddleware())

@router.callback_query(F.data == "admin_manage")
async def admin_manage(query: CallbackQuery, state: FSMContext):
    await query.answer()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить пользователя", callback_data="add_user")],
        [InlineKeyboardButton(text="Список пользователей", callback_data="list_users")],
        [InlineKeyboardButton(text="Back", callback_data="back_0")]
    ])
    text = "Выберите действие"
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await query.message.edit_text(text, reply_markup=markup)