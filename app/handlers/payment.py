import os
import logging
from dotenv import load_dotenv
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
import stripe


load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY
ADMIN_ID = ...

router = Router()

MINIMUM_AMOUNT = {
    "USD": 1.00,
    "EUR": 1.00,
    "UZS": 12000,
}

user_payment_data = {}


@router.message(Command("donate"))
async def chose_currency(message: types.Message):
    currency_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇸 USD", callback_data="currency_usd")],
            [InlineKeyboardButton(text="🇪🇺 EUR", callback_data="currency_eur")],
            [InlineKeyboardButton(text="🇺🇿 UZS", callback_data="currency_uzs")]
        ]
    )
    await message.answer("Выберите валюту для доната:", reply_markup=currency_keyboard)


@router.callback_query(F.data.startswith("currency_"))
async def choose_amount(callback: CallbackQuery):
    currency = callback.data.split("_")[1].upper()
    user_payment_data[callback.from_user.id] = {"currency": currency}

    amount_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="$5", callback_data="amount_5")],
            [InlineKeyboardButton(text="$10", callback_data="amount_10")],
            [InlineKeyboardButton(text="💰 Ввести сумму", callback_data="amount_custom")]
        ]
    )
    await callback.message.edit_text(f"Вы выбрали валюту: **{currency}**.\nТеперь выберите сумму:", reply_markup=amount_keyboard)


@router.callback_query(F.data.startswith("amount_"))
async def process_payment(callback: CallbackQuery):
    amount_data = callback.data.split("_")[1]

    if amount_data == "custom":
        await callback.message.edit_text("Введите сумму вручную (только число):")
        return
    
    amount = int(amount_data)
    user_id = callback.from_user.id
    currency = user_payment_data.get(user_id, {}).get("currency", "USD")

    if amount < MINIMUM_AMOUNT.get(currency, 1):
        await callback.message.answer(f"Минимальная сумма для {currency} — {MINIMUM_AMOUNT[currency]}.")
        return
    
    await create_payment(callback.message, user_id, amount, currency)


@router.message(F.text.isdigit())
async def process_custom_amount(message: types.Message):
    user_id = message.from_user.id
    amount = int(message.text)
    
    currency = user_payment_data.get(user_id, {}).get("currency", "USD")

    if amount < MINIMUM_AMOUNT.get(currency, 1):
        await message.answer(f"Минимальная сумма для {currency} — {MINIMUM_AMOUNT[currency]}.")
        return
    
    await create_payment(message, user_id, amount, currency)

    
async def create_payment(message: types.Message, user_id: int, amount: int, currency: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency.lower(),
                    "product_data": {"name": "Поддержка проекта"},
                    "unit_amount": amount * 100,  # Конвертация в центы
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://t.me/akromrustamov_bot?start=success",
            cancel_url="https://t.me/akromrustamov_bot?start=cancel",
        )

        # Проверяем, есть ли ссылка на оплату
        if session and session.url:
            donate_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"💳 Оплатить {amount} {currency}", 
                        url=session.url
                        # web_app=WebAppInfo(url=session.url) # Открывает URL в Telegram Web App
                    )]
                ]
            )
            await message.answer(
                f"Вы выбрали донат на **{amount} {currency}**.\nПерейдите по ссылке для оплаты:",
                reply_markup=donate_keyboard
            )
        else:
            await message.answer("❌ Ошибка при создании платежной сессии. Попробуйте позже.")

    except Exception as e:
        logging.exception("Ошибка при создании платежной сессии Stripe")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
