from aiogram import Dispatcher
from .base import router as base_router
from .ai import router as ai_router
from .feedback import router as feedback_router
from .payment import router as payment_router


def register_all_handlers(dp: Dispatcher):
    dp.include_router(base_router)
    dp.include_router(ai_router)
    dp.include_router(feedback_router)
    dp.include_router(payment_router)
