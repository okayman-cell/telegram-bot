from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from storage import warnings  # импортируем один общий словарь

router = Router()

BAD_WORDS = ["блять", "сука", "нахуй", "пизда", "хуй", "ебать"]
MAX_WARNINGS = 3


@router.message()
async def warn_system(msg: Message):
    if not msg.text:
        return

    text = msg.text.lower()

    if any(word in text for word in BAD_WORDS):

        user_id = msg.from_user.id
        warnings[user_id] = warnings.get(user_id, 0) + 1
        warn_count = warnings[user_id]

        await msg.answer(
            f"⚠️ {msg.from_user.full_name}, предупреждение {warn_count}/{MAX_WARNINGS}."
        )


@router.message(Command("warns"))
async def show_warns(msg: Message):
    if not warnings:
        await msg.answer("📭 Предупреждений нет.")
        return

    text = "📋 Список предупреждений:\n\n"

    for user_id, count in warnings.items():
        text += f"• ID {user_id} — {count} предупреждений\n"

    await msg.answer(text)
