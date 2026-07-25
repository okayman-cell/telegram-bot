from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
import asyncio
import os
import random
from datetime import timedelta
import time




import os 
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()
########
import random


QUOTES = [
    "Не ошибается тот, кто ничего не делает.",
    "Успех приходит к тем, кто действует.",
    "Каждый день — новый шанс стать лучше.",
    "Сила в том, чтобы не сдаваться.",
    "Лучшее время начать — сейчас."
]

@dp.message(Command("quote"))
async def quote(msg: Message):
    text = random.choice(QUOTES)
    await msg.answer(f"💬 {text}")



######
@dp.message(Command("coin"))
async def coin(msg: Message):
    result = random.choice(["Орёл 🦅", "Решка 🎯"])
    await msg.answer(f"🪙 Монета: {result}")



#####
# Глобальный словарь варнов
warnings = {}

MAX_WARNINGS = 3

@dp.message(Command("warn"))
async def warn(msg: Message):
    # Проверяем, есть ли реплай
    if not msg.reply_to_message:
        await msg.answer("⚠️ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id

    # Добавляем предупреждение
    warnings[user_id] = warnings.get(user_id, 0) + 1
    warn_count = warnings[user_id]

    await msg.answer(
        f"⚠️ {user.full_name} получил предупреждение {warn_count}/{MAX_WARNINGS}."
    )

#####


@dp.message(Command("clear"))
async def clear_warns(msg: Message):
    # Команда должна быть в ответ на сообщение
    if not msg.reply_to_message:
        await msg.answer("❗ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id

    # Если у пользователя нет варнов
    if user_id not in warnings:
        await msg.answer(f"ℹ️ У {user.full_name} нет предупреждений.")
        return

    # Сбрасываем варны
    warnings[user_id] = 0

    await msg.answer(f"✅ Предупреждения пользователя {user.full_name} сброшены.")



#####




# Глобальный словарь варнов
warnings = {}

# Список запрещённых слов
BAD_WORDS = ["блять", "сука", "нахуй", "пизда", "хуй", "ебать","бля"]

MAX_WARNINGS = 3   # после 3 варнов — мут
MUTE_TIME = 60      # минут


@dp.message()
async def antimat_system(msg: Message):
    if not msg.text:
        return

    text = msg.text.lower()

    # Проверяем мат
    if any(word in text for word in BAD_WORDS):

        user_id = msg.from_user.id

        # Добавляем варн
        warnings[user_id] = warnings.get(user_id, 0) + 1
        warn_count = warnings[user_id]

        # Сообщение о варне
        await msg.answer(
            f"⚠️ {msg.from_user.full_name}, предупреждение {warn_count}/{MAX_WARNINGS}."
        )

        # Если достигнут лимит — мут
        if warn_count >= MAX_WARNINGS:
            try:
                await msg.bot.restrict_chat_member(
                    msg.chat.id,
                    user_id,
                    permissions={"can_send_messages": False},
                    until_date=timedelta(minutes=MUTE_TIME)
                )

                await msg.answer(
                    f"🔇 {msg.from_user.full_name} получил мут на {MUTE_TIME} минут."
                )

                # Сбрасываем варны после мута
                warnings[user_id] = 0

            except Exception as e:
                await msg.answer("❗ Не удалось выдать мут. Возможно, у бота нет прав.")
                print(e)
#####


####
####



@dp.message(Command("ping"))
async def ping(msg: Message):
    start = time.time()

    reply = await msg.answer("🏓 Pong!")
    end = time.time()

    ping_ms = int((end - start) * 1000)

    await reply.edit_text(f"🏓 Pong! ({ping_ms} ms)")


#####


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот запущен!")

@dp.message(Command("mute"))
async def mute_user(msg: Message):
    # Команда должна быть в ответ на сообщение
    if not msg.reply_to_message:
        await msg.answer("❗ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id

    # Время мута (в минутах)
    MUTE_TIME = 2400

    try:
        await msg.bot.restrict_chat_member(
            msg.chat.id,
            user_id,
            permissions={"can_send_messages": False},
            until_date=timedelta(minutes=MUTE_TIME)
        )

        await msg.answer(f"🔇 {user.full_name} получил мут на {MUTE_TIME} минут.")

    except Exception as e:
        await msg.answer("❗ Не удалось выдать мут. У бота нет прав.")
        print(e)

@dp.message(Command("unmute"))
async def unmute_user(msg: Message):
    if not msg.reply_to_message:
        await msg.answer("❗ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id

    try:
        await msg.bot.restrict_chat_member(
            msg.chat.id,
            user_id,
            permissions={"can_send_messages": True}
        )

        await msg.answer(f"🔊 {user.full_name} теперь может писать сообщения.")

    except Exception as e:
        await msg.answer("❗ Не удалось снять мут. У бота нет прав.")
        print(e)

@dp.message(Command("help"))
async def help_cmd(msg: Message):
    text = (
        "📘 *Список команд бота:*\n\n"
        "⚠️ /warn — выдать предупреждение (в ответ на сообщение)\n"
        "🧹 /clear — сбросить варны пользователя (в ответ)\n"
        "🪙 /coin — орёл или решка\n"
        "💬 /quote — случайная цитата\n"
        "🏓 /ping — проверить задержку бота\n"
        "🔇 Автоматический мут после 3 варнов\n"
        "\n"
        "/help — дурка едет тебя спосать!"
    )

    await msg.answer(text, parse_mode="Markdown")

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
