import config
import asyncio
import telebot
from telebot import util
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(config.token)

class Car:
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand

    def info(self):
        return f"Машина марки {self.brand} цвета {self.color}."

user_data = {}
@bot.message_handler(commands=['car'])
async def handle_car(message):
    user_data[message.chat.id] = {"step": "color"}
    await bot.reply_to(message, "Введите цвет автомобиля:")

@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id]["step"] == "color")
async def handle_color(message):
    user_data[message.chat.id]["color"] = message.text
    user_data[message.chat.id]["step"] = "brand"
    await bot.reply_to(message, "Введите марку автомобиля:")

@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id]["step"] == "brand")
async def handle_brand(message):
    user_data[message.chat.id]["brand"] = message.text
    color = user_data[message.chat.id]["color"]
    brand = user_data[message.chat.id]["brand"]
    car = Car(color, brand)
    await bot.reply_to(message, car.info())
    del user_data[message.chat.id]


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)
@bot.message_handler(commands=['donate'])
async def donate_handler(message):
    text = 'Thank you, but I dont require money.'
    await bot.reply_to(message, text)
@bot.message_handler(commands=['info'])
async def send_info(message):
    text = 'Hi, I am EchoBot.I am your echo. I will mirror your every single message!'
    await bot.reply_to(message, text)






# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


asyncio.run(bot.polling())