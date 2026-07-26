from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
import asyncio
import os
import random
from datetime import timedelta
import time

# ------------------ TOKEN ------------------

TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()

# ------------------ ЦИТАТЫ ------------------

QUOTES = [
    "Не ошибается тот, кто ничего не делает.",
    "Успех приходит к тем, кто действует.",
    "Каждый день — новый шанс стать лучше.",
    "Сила в том, чтобы не сдаваться.",
    "Лучшее время начать — сейчас."
]

@dp.message(Command("quote"))
async def quote(msg: Message):
    await msg.answer(f"💬 {random.choice(QUOTES)}")

# ------------------ МОНЕТКА ------------------

@dp.message(Command("coin"))
async def coin(msg: Message):
    result = random.choice(["Орёл 🦅", "Решка 🎯"])
    await msg.answer(f"🪙 Монета: {result}")

# ------------------ ВАРНЫ ------------------

warnings = {}
MAX_WARNINGS = 3

@dp.message(Command("warn"))
async def warn(msg: Message):
    if not msg.reply_to_message:
        await msg.answer("⚠️ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id

    warnings[user_id] = warnings.get(user_id, 0) + 1
    warn_count = warnings[user_id]

    await msg.answer(f"⚠️ {user.full_name} получил предупреждение {warn_count}/{MAX_WARNINGS}.")

@dp.message(Command("clear"))
async def clear_warns(msg: Message):
    if not msg.reply_to_message:
        await msg.answer("❗ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id

    if user_id not in warnings:
        await msg.answer(f"ℹ️ У {user.full_name} нет предупреждений.")
        return

    warnings[user_id] = 0
    await msg.answer(f"✅ Предупреждения пользователя {user.full_name} сброшены.")

@dp.message(Command("warns"))
async def show_warns(msg: Message):
    if not warnings:
        await msg.answer("📭 Предупреждений нет.")
        return

    text = "📋 Список предупреждений:\n\n"
    for user_id, count in warnings.items():
        text += f"• ID {user_id} — {count} предупреждений\n"

    await msg.answer(text)

# ------------------ АНТИМАТ + АВТОМУТ ------------------

BAD_WORDS = ["блять", "сука", "нахуй", "пизда", "хуй", "ебать", "бля"]
AUTO_MUTE_TIME = 60  # минут

@dp.message()
async def antimat_system(msg: Message):
    if not msg.text:
        return

    text = msg.text.lower()

    if any(word in text for word in BAD_WORDS):
        user_id = msg.from_user.id

        warnings[user_id] = warnings.get(user_id, 0) + 1
        warn_count = warnings[user_id]

        await msg.answer(f"⚠️ {msg.from_user.full_name}, предупреждение {warn_count}/{MAX_WARNINGS}.")

if warn_count >= MAX_WARNINGS:
    try:
        await msg.bot.restrict_chat_member(
            chat_id=msg.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=timedelta(minutes=MUTE_TIME)
        )

        await msg.answer(
            f"🔇 {msg.from_user.full_name} получил мут на {MUTE_TIME} минут."
        )

        warnings[user_id] = 0
    except Exception as e:
        await msg.answer("❗ Не удалось выдать мут. Возможно, у бота нет прав.")
        print(e)


            await msg.answer(f"🔇 {msg.from_user.full_name} получил мут на {AUTO_MUTE_TIME} минут.")
            warnings[user_id] = 0

            except Exception as e:
                await msg.answer("❗ Не удалось выдать мут. Возможно, у бота нет прав.")
                print(e)

# ------------------ ПИНГ ------------------

@dp.message(Command("ping"))
async def ping(msg: Message):
    start = time.time()
    reply = await msg.answer("🏓 Pong!")
    end = time.time()

    ping_ms = int((end - start) * 1000)
    await reply.edit_text(f"🏓 Pong! ({ping_ms} ms)")

# ------------------ СТАРТ ------------------

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот запущен!")

# ------------------ МУТ / УНМУТ ------------------

@dp.message(Command("mute"))
async def mute_user(msg: Message):
    if not msg.reply_to_message:
        await msg.answer("❗ Используй команду в ответ на сообщение пользователя.")
        return

    user = msg.reply_to_message.from_user
    user_id = user.id
    MUTE_TIME = 2400  # минут

    try:
        await msg.bot.restrict_chat_member(
            chat_id=msg.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
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
            chat_id=msg.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await msg.answer(f"🔊 {user.full_name} теперь может писать сообщения.")

    except Exception as e:
        await msg.answer("❗ Не удалось снять мут. У бота нет прав.")
        print(e)

# ------------------ HELP ------------------

@dp.message(Command("help"))
async def help_cmd(msg: Message):
    text = (
        "📘 *Команды бота:*\n\n"
        f"⚠️ /warn — выдать предупреждение ({'[warn](ca://s?q=warn)'} )\n"
        f"🧹 /clear — сбросить варны ({'[clear](ca://s?q=clear)'} )\n"
        f"📋 /warns — список предупреждений ({'[warns](ca://s?q=warns)'} )\n"
        f"🪙 /coin — монетка ({'[coin](ca://s?q=coin)'} )\n"
        f"💬 /quote — цитата ({'[quote](ca://s?q=quote)'} )\n"
        f"🏓 /ping — задержка ({'[ping](ca://s?q=ping)'} )\n"
        f"🔇 /mute — мут ({'[mute](ca://s?q=mute)'} )\n"
        f"🔊 /unmute — размут ({'[unmute](ca://s?q=unmute)'} )\n"
        f"👢 /del — удалить сообщение ({'[del](ca://s?q=del)'} )\n"
        "\n"
        "Анти‑мат и авто‑мут включены."
    )

    await msg.answer(text, parse_mode="Markdown")

# ------------------ УДАЛЕНИЕ СООБЩЕНИЯ ------------------

@dp.message(Command("del"))
async def delete_msg(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя.")
        return

    msg_id = message.reply_to_message.message_id
    await bot.delete_message(message.chat.id, msg_id)

    await message.answer("👢 Сообщение удалено.")

# ------------------ ЗАПУСК ------------------

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

