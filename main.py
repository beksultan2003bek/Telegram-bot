import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Konfiguratsiya
API_TOKEN = '8250343871:AAGPIcIcXyyQsXvQ6mRkR2LLRZXSw8vFLek'
ADMIN_ID = 855204630

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Xabarlarni log qilish (xatolikni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Xush kelibsiz! Bot faol.")

# Foydalanuvchidan adminga xabar yuborish (Rasm, Video, Matn va h.k)
@dp.message(F.chat.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    # Foydalanuvchi ma'lumotlarini tayyorlash
    user_info = (
        f"📩 Yangi xabar!\n"
        f"👤 Kimdan: {message.from_user.full_name}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username}\n"
        f"---"
    )
    
    # Avval foydalanuvchi haqida ma'lumot yuboramiz
    await bot.send_message(ADMIN_ID, user_info)
    
    # Xabarning o'zini adminga nusxalaymiz (copy_to)
    # Bu usulda rasm ostidagi yozuvlar ham birga boradi
    await message.copy_to(chat_id=ADMIN_ID)

# Admindan foydalanuvchiga javob yuborish
# Admin xabarga "Reply" (javob berish) qilishi shart
@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def reply_to_user(message: types.Message):
    try:
        # Reply qilingan xabardan foydalanuvchi ID sini topamiz
        # Buning uchun admin xabarining originalidan ID ni ajratish kerak
        # Eng oson yo'li: admin xabarni nusxalash orqali yuborganimizda, 
        # reply qilingan xabarning matnidan ID ni qidiramiz
        
        # Diqqat: Bu kodda admin foydalanuvchi xabariga reply bossagina ishlaydi
        target_id = None
        
        # Agar admin foydalanuvchi yuborgan "copy" qilingan xabarga reply qilsa:
        if message.reply_to_message.forward_from:
            target_id = message.reply_to_message.forward_from.id
        else:
            # Agar forward yopiq bo'lsa, xabardagi ID ni aniqlash (oddiyroq usul)
            # Bu yerda admin faqat xabarga reply qilsa bot o'sha xabarni qaytaradi
            await message.copy_to(chat_id=message.reply_to_message.forward_from_chat.id if message.reply_to_message.forward_from_chat else message.reply_to_message.from_user.id)
            return

        await message.copy_to(chat_id=target_id)
        await message.answer("Xabar yuborildi ✅")
    except Exception as e:
        await message.answer(f"Xatolik: Xabarni yuborib bo'lmadi. Foydalanuvchi botni bloklagan bo'lishi mumkin.")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
