from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile

from db.psql.enums.enums import Roles
from middleware import MsgMiddleware, CallbackMiddleware
from utils.course_util import course_data, get_module_by_id, get_lection_by_id

router = Router()
router.message.middleware(MsgMiddleware([Roles.ADMIN, Roles.STUDENT]))
router.callback_query.middleware(CallbackMiddleware([Roles.ADMIN, Roles.STUDENT]))


def course_module_markup(with_back: bool = True):
    buttons = [
        [InlineKeyboardButton(text=module.get("name"), callback_data=f"module_{module.get('id')}")] for module in
        course_data.get("modules")
    ]
    if with_back:
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_0")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("course"))
async def course1(message: Message, state: FSMContext):
    markup = course_module_markup(False)
    text = course_data.get("name")
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await message.answer(text, reply_markup=markup)


@router.callback_query(F.data == "courses")
async def course2(query: CallbackQuery, state: FSMContext):
    markup = course_module_markup()
    text = course_data.get("name")
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await (query.message.edit_text(text, reply_markup=markup))


@router.callback_query(F.data.startswith("module_"))
async def module_by_id(query: CallbackQuery, state: FSMContext):
    module_id = int(query.data.split("_")[1])
    module = get_module_by_id(module_id)
    if not module:
        await query.answer("Модуль не найден", show_alert=True)
        return
    text = module.get("name")
    markup = [
        [InlineKeyboardButton(text=lection.get("name"), callback_data=f"lection_{module_id}_{lection.get('id')}")] for
        lection in module.get("lections")
    ]
    markup.append([InlineKeyboardButton(text="Назад", callback_data="back_1")])
    markup = InlineKeyboardMarkup(inline_keyboard=markup)
    await state.update_data(bt2=text)
    await state.update_data(br2=markup)
    await query.message.edit_text(text, reply_markup=markup)


@router.callback_query(F.data.startswith("lection_"))
async def lection_by_id(query: CallbackQuery):
    _, module_id, lection_id = query.data.split("_")
    lection = get_lection_by_id(int(module_id), int(lection_id))
    if not lection:
        await query.answer("Лекция не найдена", show_alert=True)
        return
    file = FSInputFile(path=lection.get("path"))
    await query.message.delete()
    text = lection.get("name")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"back_2")]
    ])
    await query.message.answer_video(file, caption=text, protect_content=True, reply_markup=markup)
