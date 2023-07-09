import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
from datetime import datetime, timedelta

from config import TOKEN
#api_key = '070bade5b4a6b3a83e490c432173d763'

# Устанавливаем уровень логов на уровне INFO
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot_token = TOKEN
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)




















# Класс состояний
class WeatherStates(StatesGroup):
    waiting_for_city = State()

# Обработчик команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    # Получаем погодные данные для Барселоны
    weather_data = get_weather("Barcelona")

    if weather_data:
        # Форматируем погодные данные в нужный формат
        formatted_weather = format_weather(weather_data)

        # Отправляем пользователю погодные данные
        await message.answer(formatted_weather)
    else:
        # Сообщаем, что не удалось получить погоду
        await message.answer("Не удалось получить погоду. Попробуйте еще раз.")

# Функция для получения погодных данных из API
def get_weather(city):
    api_key = '070bade5b4a6b3a83e490c432173d763'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    response = requests.get(url)
    data = response.json()

    if data['cod'] == '200':
        return data['list']
    else:
        return None

# Функция для форматирования погодных данных
def format_weather(weather_data):
    formatted_weather = ""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Фильтруем погодные данные только для завтрашнего дня и нужных времен
    tomorrow_weather = [weather for weather in weather_data if weather['dt_txt'].startswith(tomorrow) and weather['dt_txt'].endswith(('09:00:00', '15:00:00', '21:00:00'))]

    for weather in tomorrow_weather:
        # Получаем информацию о времени и погоде
        time = get_time_period(weather['dt_txt'])
        temperature = round(weather['main']['temp'])
        humidity = weather['main']['humidity']
        description = weather['weather'][0]['description']
        wind_direction, wind_arrow = get_wind_direction(weather['wind']['deg'])
        emoji = get_weather_emoji(description)

        # Формируем строку с погодой
        formatted_weather += f"{time}, {emoji}, 🌡️ +{temperature}°C, Влажность: {humidity}%, {wind_direction}\n"

    return formatted_weather

# Функция для определения временного периода
def get_time_period(dt_txt):
    time = dt_txt.split(' ')[1]

    if time == '09:00:00':
        return 'Утро'
    elif time == '15:00:00':
        return 'День'
    elif time == '21:00:00':
        return 'Вечер'

    return ''

# Функция для определения направления ветра и стрелки
def get_wind_direction(deg):
    if 337.5 <= deg < 22.5:
        return 'Северный', '↑'
    elif 22.5 <= deg < 67.5:
        return 'Северо-восточный', '↗'
    elif 67.5 <= deg < 112.5:
        return 'Восточный', '→'
    elif 112.5 <= deg < 157.5:
        return 'Юго-восточный', '↘'
    elif 157.5 <= deg < 202.5:
        return 'Южный', '↓'
    elif 202.5 <= deg < 247.5:
        return 'Юго-западный', '↙'
    elif 247.5 <= deg < 292.5:
        return 'Западный', '←'
    elif 292.5 <= deg < 337.5:
        return 'Северо-западный', '↖'

    return '', ''

# Функция для получения эмодзи в зависимости от описания погоды
def get_weather_emoji(description):
    emojis = {
        'clear sky': '☀️',
        'light rain': '🌧️',
        'scattered clouds': '⛅',
        'broken clouds': '☁️',
        'overcast clouds': '☁️',
        'moderate rain': '🌧️',
        'few clouds': '🌤️'
    }

    return emojis.get(description, '')

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)