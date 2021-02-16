from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import random
import sqlite3

bot = Bot(token = '1619867027:AAEkQ8hi7R9w9QrfHqTl3yE9TUeV2fMzXHU')
dp = Dispatcher(bot)


db = sqlite3.connect("database2.db")
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS podarki (
            podarok TEXT
            )""")

db.commit()


@dp.message_handler(content_types = ['text'])
async def add(message: types.Message):
    if message.text == '/start':
        await bot.send_message(message.from_user.id, "Привет, для добавления подарка просто введите его название, я автоматически запишу (ничего другого писать не нужно)\nДля показа всего списка введите /showall\n Для выдачи подарка введите /random\nДля удаления всего списка введите команду /deleteall\n")
    elif message.text == '/showall':
        sql.execute("DELETE FROM podarki WHERE podarok = '/showall'")
        db.commit()

        sql.execute("SELECT podarok FROM podarki")

        result = sql.fetchall()
        await bot.send_message(message.from_user.id, result)
    elif message.text == '/deleteall':
        sql.execute("DELETE FROM podarki")
        db.commit()
        await bot.send_message(message.from_user.id, "Всё успешно удалено!")
    elif message.text == '/random':
        rand = sql.execute("SELECT podarok FROM podarki ORDER BY random() LIMIT 1")
        result2 = sql.fetchone()
        await bot.send_message(message.from_user.id, result2[0])
        
    else:
        sql.execute("INSERT INTO podarki(podarok) VALUES(?)", [message.text])
        await bot.send_message(message.from_user.id, "Ваш подарок успешно добавлен в список!")
        db.commit()


if __name__ == '__main__':
    executor.start_polling(dp)