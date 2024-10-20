import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from googletrans import Translator
import re

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# Инициализация бота, диспетчера и хранилища состояний
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
translator = Translator()  # Инициализация переводчика

# Класс состояний
class FactState(StatesGroup):
    fact_type = State()  # Состояние для хранения типа факта

# Создаем кнопки с обновленными названиями
buttons = [
    [KeyboardButton(text="Факт из жизни"), KeyboardButton(text="Математический факт")],
    [KeyboardButton(text="Факт о годе"), KeyboardButton(text="Факт о дате")]
]
keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Проверка, является ли введенная строка корректной датой
def is_valid_date(date_str):
    return re.match(r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$", date_str)

# Проверка, является ли введенная строка годом
def is_valid_year(year_str):
    return year_str.isdigit() and len(year_str) == 4

# Получение информации с сайта NumbersAPI и перевод на русский язык
async def get_fact_and_translate(number, fact_type):
    # Преобразуем тип факта в нужный формат для API
    fact_type_en = {
        "Факт из жизни": "trivia",
        "Математический факт": "math",
        "Факт о годе": "year",
        "Факт о дате": "date"
    }[fact_type]

    url = f'http://numbersapi.com/{number}/{fact_type_en}'
    response = requests.get(url)
    if response.status_code == 200:
        fact_in_english = response.text
        # Переводим факт на русский язык
        translation = translator.translate(fact_in_english, src='en', dest='ru').text
        return translation
    return "Не удалось получить информацию."

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name} меня зовут Ларс!!! \n"
                         f" Я знаю кучу фактов о числах и с удовольствием поделюсь своими зананиями \n"
                         f"Выберите тип факта, а затем введите число.", reply_markup=keyboard)

# Обработчик выбора типа факта
@dp.message(lambda message: message.text in ["Факт из жизни", "Математический факт", "Факт о годе", "Факт о дате"])
async def handle_fact_type(message: types.Message, state: FSMContext):
    fact_type = message.text
    await state.update_data(fact_type=fact_type)
    await message.answer(f"Введите число для типа {fact_type}:")

# Обработчик ввода числа
@dp.message(lambda message: message.text.isdigit() or "/" in message.text)
async def handle_number_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    fact_type = user_data.get("fact_type")

    # Проверка на выбор типа факта
    if not fact_type:
        await message.answer("Сначала выберите тип факта.")
        return

    # Обработка типов "Факт о годе" и "Факт о дате"
    if fact_type == "Факт о годе":
        if is_valid_year(message.text):
            fact = await get_fact_and_translate(message.text, fact_type)
            await message.answer(fact)
        else:
            await message.answer("Введите корректный год (4 цифры).")
    elif fact_type == "Факт о дате":
        if is_valid_date(message.text):
            fact = await get_fact_and_translate(message.text, fact_type)
            await message.answer(fact)
        else:
            await message.answer("Введите корректную дату в формате MM/DD.")
    else:
        # Для типов "Факт из жизни" и "Математический факт" не требуется дополнительных проверок
        fact = await get_fact_and_translate(message.text, fact_type)
        await message.answer(fact)

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
