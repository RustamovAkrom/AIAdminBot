from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apps.bot.services import feedback

router = Router()
api_feedback = feedback.FeedbackService()


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
    user_id = message.from_user.id
    feedback_message = message.text

    if api_feedback.create_feedback(user_id, feedback_message):
        await message.answer("✅ Спасибо за ваш отзыв! Он отправлен!")
    else:
        await message.answer("❌ Произошла ошибка при отправке отзыва.")

    await state.clear()