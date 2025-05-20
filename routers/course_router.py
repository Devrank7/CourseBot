from aiogram import Router

from db.psql.enums.enums import Roles
from middleware import MsgMiddleware, CallbackMiddleware

router = Router()

router.message.middleware(MsgMiddleware([Roles.ADMIN, Roles.STUDENT]))
router.callback_query.middleware(CallbackMiddleware([Roles.ADMIN, Roles.STUDENT]))