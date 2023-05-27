 
from config import TOKEN
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import asyncio
import datetime
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot_token = TOKEN
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
#chat = '-1001655157125' # Barselona
#chat = '-1001339593916'
chat = '-961987561'
class WeatherStates(StatesGroup):
    waiting_for_weather = State()


#@dp.message_handler(commands=['weather'])
#async def send_weather(message: types.Message):
#    response = requests.get('https://wttr.in/Barcelona?format=%l:+%c+%t+%m+%z')
#    weather_data = response.text
#    #city = 'Barcelona'  # Change the city name as per your requirement
#    foto = f'https://wttr.in/Barcelona_3tqp_lang=ru.png?theme=dark'
#    await bot.send_photo(message.chat.id, photo=foto, caption=f"{weather_data}")

 

#@dp.message_handler(commands=['start'])
async def send_weatherr(message: types.Message):
    response = requests.get('https://v1.wttr.in/Barcelona_M_lang=ru.png')
    response1 = requests.get('https://v2.wttr.in/Barcelona_M_lang=ru.png')
    response_text = requests.get('https://ru.wttr.in/Barcelona?format=%l:\n+%C+%c+%t\n+Влажность   \t+%h\n+Ветер              +%w')
                                 #\n+Фаза луны/день +%m+%M\n+Давление %P\n+UV index %u')
    weather_data = response_text.text
    # Отправка фотографии
    await bot.send_photo(chat, photo=response.content)
    await bot.send_photo(chat, photo=response1.content, caption=f"{weather_data}")


async def scheduled_weather():
    while True:
        now = datetime.datetime.now()
        if now.hour == 21 and now.minute == 36:
            await send_weatherr(types.Message)
        await asyncio.sleep(60)  # Проверка каждую минуту

 


 

if __name__ == '__main__':
    from aiogram import executor
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_weather())
    # Запуск бота
    executor.start_polling(dp)

