from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()


class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()


@router.message(Command("feedback"))
async def feedback_start(message: types.Message, state: FSMContext):
    await message.answer(
        "📝 Напишите свой отзыв или предложение. Я его обязательно прочту!"
    )
    await state.set_state(FeedbackForm.waiting_for_feedback)


@router.message(FeedbackForm.waiting_for_feedback)
async def feedback_received(message: types.Message, state: FSMContext):
    # Здесь можно добавить сохранение отзыва в базу Django
    await message.answer("✅ Спасибо за ваш отзыв! Он очень важен для меня.")
    await state.clear()
