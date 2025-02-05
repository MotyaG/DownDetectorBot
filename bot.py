from parser import Parser
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from database import Database
import asyncio

bot = Bot("TOKEN")
dp = Dispatcher()
db = Database("database.db")

timer_task = None
stop_event = asyncio.Event()

async def parse_and_send(message: types.Message):
    parser = Parser()
    results = await parser.parse(['bank', 'media', 'telecom', 'chats', 'market',
                            'gos', 'regions', 'games', 'it', 'betting', 
                            'communal', 'industry', 'education', 'travel',
                            'retail', 'construction', 'logistics', 
                            'smarthouse', 'buisiness', 'vpn', 'billboards',
                            'fun', 'ai'])
    for result in results:
        if db.check_site(result):
            print("Already in database.")
        else:
            db.add_site(result)
            await message.answer(f'🔴 У СЕРВИСА "{result}" НАБЛЮДАЮТСЯ ПРОБЛЕМЫ 🔴')

async def timer(message: types.Message):
    while not stop_event.is_set():
        print("Выполняем...")
        await parse_and_send(message)
        print("Ожидаем...")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=600)
        except asyncio.TimeoutError:
            continue
    print("Процесс остановлен.")

@dp.message(Command("run"))
async def run(message: types.Message):
    if message.from_user.id == 1700698354:
        global timer_task
        if timer_task and not timer_task.done():
            await message.answer("Процесс уже запущен!")
            return
        
        stop_event.clear()
        timer_task = asyncio.create_task(timer(message))
        await message.answer("Процесс запущен!")
    else:
        await message.answer("Вы не администратор!")

@dp.message(Command("clear"))
async def clear(message: types.Message):
    if message.from_user.id == 1700698354:
        db.remove_db()
        db.create_db()
        await message.answer("База данных очищена!")
    else:
        await message.answer("Вы не администратор!")

@dp.message(Command("stop"))
async def stop(message: types.Message):
    if message.from_user.id == 1700698354:
        if not stop_event.is_set():
            stop_event.set()
            await message.answer("Процесс остановлен!")
        else:
            await message.answer("Процесс уже остановлен.")
    else:
        await message.answer("Вы не администратор!")

async def run():
    print("Bot started!")
    await dp.start_polling(bot)
