from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
import asyncio

import os 
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()
########
from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Глобальный словарь варнов
warnings = {}

# Список мата
BAD_WORDS = ["блять", "сука", "нахуй", "пизда", "хуй", "ебать"]

MAX_WARNINGS = 3


@router.message()
async def warn_system(msg: Message, bot: Bot):
    # Если нет текста — игнорируем
    if not msg.text:
        return

    text = msg.text.lower()

    # Проверяем мат
    if any(word in text for word in BAD_WORDS):

        # Удаляем сообщение
        await bot.delete_message(msg.chat.id, msg.message_id)

        user_id = msg.from_user.id

        # Добавляем предупреждение
        warnings[user_id] = warnings.get(user_id, 0) + 1
        warn_count = warnings[user_id]

        # Выводим предупреждение
        await msg.answer(
            f"⚠️ {msg.from_user.full_name}, предупреждение {warn_count}/{MAX_WARNINGS}."
        )


@router.message(Command("warns"))
async def show_warns(msg: Message, bot: Bot):
    if not warnings:
        await msg.answer("📭 Предупреждений нет.")
        return

    text = "📋 Список предупреждений:\n\n"

    for user_id, count in warnings.items():
        try:
            user = await bot.get_chat_member(msg.chat.id, user_id)
            name = user.user.full_name
        except:
            name = f"ID {user_id}"

        text += f"• {name} — {count} предупреждений\n"

    await msg.answer(text)



#####
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот запущен!")

@dp.message(Command("mute"))
async def mute(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя.")
        return

    user = message.reply_to_message.from_user.id

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user,
        permissions=ChatPermissions(
            can_send_messages=False
        )
    )

    await message.answer("🔇 Пользователь замучен.")

@dp.message(Command("unmute"))
async def unmute(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя.")
        return

    user = message.reply_to_message.from_user.id

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_documents=True,
            can_send_other_messages=True
        )
    )

    await message.answer("🔊 Пользователь размучен.")

@dp.message(Command("Help"))
async def ban(message: Message):
    if not message.reply_to_message:
        await message.answer(" бот сам ловит маты и у него есть команды: /mute -- мут навседа,/unmute -- унмут если ктота был замучен ,/del -- удалить когото сообщение ,/Help -- помощь ,/warns -- посмотреть варны .")
        return

  

    await message.answer("/mute -- мут навседа,/unmute -- унмут если ктота был замучен ,/rep -- удалить когото сообщение ,/Help -- помощь.")

@dp.message(Command("del"))
async def kick(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя.")
        return

    user = message.reply_to_message.from_user.id

    
    await bot.delete_message(message.chat.id, user)

    await message.answer("👢сообщение удалено.")

async def main():
    print("hello!! this is group management bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
