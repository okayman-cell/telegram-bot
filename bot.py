from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
import asyncio
dp.include_router(router)


import os 
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()
########


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
