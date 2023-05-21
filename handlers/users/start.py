import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart


from data.config import ADMINS
from loader import dp,db,bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user=await db.add_user(telegram_id=message.from_user.id,
                               username=message.from_user.username,
                               full_name=message.from_user.full_name)

    except asyncpg.exceptions.UniqueViolationError:
        user=db.select_user(telegram_id=message.from_user.id)


    await message.answer("Assalomu alaykum botga Xush Kelibsiz")


    #Adminga Xabar beramiz
    count=await db.count_users()
    msg=f"{message.from_user.full_name} bazaga qo'shildi bazada \n{count} ta foydalanuvchi bor"
    await bot.send_message(ADMINS[0],msg)




@dp.message_handler(commands='sanoq',user_id=ADMINS[0])
async def select_count(message:types.Message):
    count=await db.count_users()
    await message.reply(f"ADMIN bazada :{count} ta foydalanuvchi bor")



