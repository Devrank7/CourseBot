from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db.psql.enums.enums import Roles
from db.psql.service import run_sql, ReadUsersByRole, ReadUserByUsername
from keyboards.keyboards import ListKeyboardMarkup

router = Router()

@router.callback_query(F.data == "list_users")
async def list_users(query: CallbackQuery, state: FSMContext):
    users = await run_sql(ReadUsersByRole([Roles.STUDENT]))
    markup = ListKeyboardMarkup(users, lambda user: f"@{user.username}", lambda user: user.username, "user_", True, 1).as_keyboard_markup()
    text = "Выберите пользователя"
    await state.update_data(bt2=text)
    await state.update_data(br2=markup)
    await query.message.edit_text(text, reply_markup=markup)

@router.callback_query(F.data.startswith("user_"))
async def user_info(query: CallbackQuery, state: FSMContext):
    username = query.data.split("_")[1]
    user = await run_sql(ReadUserByUsername(username))
    if user is None:
        await query.answer("Пользователь не найден", show_alert=True)
        return
    text = f'''Имя: {user.first_name}\n
               Фамилия: {user.last_name}\n
               Username: @{user.username}
            '''
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить пользователя", callback_data=f"delete_user_{user.username}")],
        [InlineKeyboardButton(text="Back", callback_data="back_2")]
    ])
    await state.update_data(bt3=text)
    await state.update_data(br3=markup)
    await query.message.edit_text(text, reply_markup=markup)