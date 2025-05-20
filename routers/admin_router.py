from aiogram import Router

from middleware import MsgMiddleware, CallbackMiddleware

router = Router()

router.message.middleware(MsgMiddleware())
router.callback_query.middleware(CallbackMiddleware())