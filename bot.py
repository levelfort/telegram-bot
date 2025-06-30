from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = '7841129888:AAEgfnw6gLMkEjffWtl_e0PH3kJtWfsSjMo'
CHANNEL_ID = '@KinoSovet4ik'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Тестовая база фильмов
movie_db = {
    "0001": "Матрица",
    "0002": "Начало",
    "0003": "Интерстеллар",
}


async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False


# 👉 Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Отправь мне код фильма, и я скажу тебе его название. "
        "Но сначала подпишись на наш канал!"
    )


# 👉 Обработчик кодов фильмов
@dp.message_handler()
async def handle_code(message: types.Message):
    user_id = message.from_user.id
    code = message.text.strip().lower()

    if not await is_subscribed(user_id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("✅ Я подписался"))

        await message.answer(
            f"❗ Чтобы получить название фильма, подпишись на канал {CHANNEL_ID} и нажми 'Я подписался'",
            reply_markup=keyboard
        )
        return

    movie = movie_db.get(code)
    if movie:
        await message.answer(f"🎬 Название фильма: {movie}")
    else:
        await message.answer("😕 Фильм с таким кодом не найден. Попробуй другой код.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
