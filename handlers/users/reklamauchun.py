
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import ADMINS
from loader import db,bot,dp


class MyState(StatesGroup):
    waiting_for_ad = State()

@dp.message_handler(Command("reklama"),user_id=ADMINS[0])
async def send_ad(message: types.Message):
    await message.answer("Reklama matnini, rasimni yoki videoni yuboring")
    await MyState.waiting_for_ad.set()

@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.PHOTO, types.ContentType.VIDEO], state=MyState.waiting_for_ad)
async def process_ad_content(message: types.Message, state: FSMContext):
    content_type = message.content_type
    await state.finish()
    users = await db.select_all_users()

    if content_type == types.ContentType.TEXT:
        text = message.text
        for user in users:
            try:
                await bot.send_message(chat_id=user['telegram_id'], text=text)
            except Exception as e:
                print(f"Matn yuborishda foydalanuvchiga xatolik yuz berdi: {e}")
    elif content_type == types.ContentType.PHOTO:
        photo = message.photo[-1]
        caption = message.caption
        for user in users:
            try:
                await bot.send_photo(chat_id=user['telegram_id'], photo=photo.file_id, caption=caption)
            except Exception as e:
                print(f"Rasim yuborishda foydalanuvchiga xatolik yuz berdi: {e}")
    elif content_type == types.ContentType.VIDEO:
        video = message.video
        caption = message.caption
        for user in users:
            try:
                await bot.send_video(chat_id=user['telegram_id'], video=video.file_id, caption=caption)
            except Exception as e:
                print(f"Video yuborishda foydalanuvchiga xatolik yuz berdi: {e}")






@dp.message_handler(commands=['count'])
async def count_users(message: types.Message):
    # Foydalanuvchilar sonini olish
    count = await db.count_users()

    # Javobni tuzish
    response = f"Bazada {count} ta foydalanuvchi bor."
    await message.reply(response)






@dp.message_handler(commands=['malumot'])
async def send_all_users_data(message: types.Message):
    # Hamma foydalanuvchilar ma'lumotlarini olish
    users = await db.select_all_users()

    # Foydalanuvchilar ma'lumotlarini formatlash va yuborish
    response = "Hamma foydalanuvchilar ma'lumotlari:\n\n"
    for user in users:
        response += f"ID: {user['id']}\n"
        response += f"Ism: {user['full_name']}\n"
        response += f"Username: {user['username']}\n"
        response += f"Telegram ID: {user['telegram_id']}\n\n"

    await message.reply(response)
