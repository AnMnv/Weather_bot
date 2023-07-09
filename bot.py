 
from config import TOKEN


chat = '-1001655157125' # Barselona
#chat = '-1001339593916'
chat2 = '-1001835619140'



import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import asyncio
import datetime
from aiogram.utils import executor

 
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests

# Устанавливаем уровень логов
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Команда /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот погоды. Введите /weather чтобы узнать погоду на завтра в Барселоне.")

# Команда /weather
@dp.message_handler(Command("weather"))
async def cmd_weather(message: types.Message):
    await WeatherForm.city.set()
    await message.reply("Введите город:")

# Обработка ответа с городом
@dp.message_handler(state=WeatherForm.city)
async def process_city(message: types.Message, state: FSMContext):
    city = message.text
    weather = get_weather(city)
    if weather is None:
        await message.reply("Не удалось получить погоду. Проверьте название города.")
    else:
        await message.reply(f"Погода в городе {city} на завтра: {weather}")
    await state.finish()

# Получение погоды
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY"
        response = requests.get(url)
        data = response.json()
        weather = data['weather'][0]['description']
        return weather
    except:
        return None

# Определение состояний
class WeatherForm(StatesGroup):
    city = State()




















async def scheduled_weather():
    while True:
        now = datetime.datetime.now()
        if now.hour == 19 and now.minute == 12:
            await send_weatherr(types.Message)
        await asyncio.sleep(60)  # Проверка каждую минуту
 


 

if __name__ == '__main__':
    from aiogram import executor
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_weather())
    # Запуск бота
    executor.start_polling(dp)
 