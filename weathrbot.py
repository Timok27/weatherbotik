import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

Api_key = 'c498b2a6e6a97305ece9b0d93181fae6'

bot = Bot(token="8161830253:AAFS4QtHnq6tSn9jRkJ1xLDiKCszvnhpmAE")
dp = Dispatcher(storage=MemoryStorage())

def get_coordinates(city):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={Api_key}'
    response = requests.get(url)
    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    return None, None

def get_weather(city):
    lat, lon = get_coordinates(city)
    if lat is not None and lon is not None:
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={Api_key}&units=metric&lang=ru'
        response = requests.get(weather_url)
        data = response.json()

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        city_name = data['name']  

        return (f"{city_name}:\n"
                f"Температура: {temp}°C\n"
                f"Влажность: {humidity}%\n"
                f"Описание: {description.capitalize()}")
    else:
        return "Город не найден"

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Введите название города, чтобы узнать погоду")

@dp.message(F.text)
async def weather(message: types.Message):
    city = message.text.strip()
    weather_info = get_weather(city)
    await message.reply(weather_info)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())