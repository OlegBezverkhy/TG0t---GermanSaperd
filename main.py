import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from config import TOKEN


# Функция для получения информации о немецкой овчарке
def get_german_shepherd_info():
    url = 'https://api.thedogapi.com/v1/breeds'
    response = requests.get(url)
    breeds = response.json()

    # Найдем породу по названию
    for breed in breeds:
        if breed['name'].lower() == 'german shepherd dog':
            breed_info = breed
            break

    # Формируем текст с информацией
    info_text = f"*Порода*: {breed_info['name']}\n"
    info_text += f"*Темперамент*: {breed_info['temperament']}\n"
    info_text += f"*Средняя продолжительность жизни*: {breed_info['life_span']}\n"
    info_text += f"*Вес*: {breed_info['weight']['metric']} кг\n"
    info_text += f"*Высота*: {breed_info['height']['metric']} см\n"

    # Рекомендации по уходу и кормлению
    care_text = "Немецкие овчарки требуют регулярного ухода за шерстью, физической активности и сбалансированного питания. " \
                "Кормление должно включать высококачественные корма с балансом белков и жиров."

    # Рекомендации по дрессировке
    training_text = "Немецкие овчарки легко обучаемы и требуют дрессировки с раннего возраста. " \
                    "Они нуждаются в умственных и физических упражнениях."

    return info_text, care_text, training_text


# Функция для получения случайного фото
def get_random_german_shepherd_photo():
    url = 'https://api.thedogapi.com/v1/images/search?breed_ids=gsd'
    response = requests.get(url)
    photo_url = response.json()[0]['url']
    return photo_url


# Обработчик команды /start
async def start(update: Update, context):
    info, care, training = get_german_shepherd_info()
    photo_url = get_random_german_shepherd_photo()

    # Отправляем информацию пользователю
    await update.message.reply_text(info, parse_mode="Markdown")
    await update.message.reply_text("*Рекомендации по уходу и кормлению*:\n" + care, parse_mode="Markdown")
    await update.message.reply_text("*Рекомендации по дрессировке*:\n" + training, parse_mode="Markdown")

    # Отправляем случайное фото
    await update.message.reply_photo(photo_url)


# Основная функция
async def main():
    # Создаем экземпляр приложения для работы с ботом
    application = ApplicationBuilder().token(TOKEN).build()

    # Обрабатываем команду /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await application.start()
    await application.idle()


# Запускаем бота
if __name__ == '__main__':
    import asyncio

    asyncio.run(main())