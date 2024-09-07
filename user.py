from pyrogram import Client, filters
import requests

# Ваш API ID, API Hash и session name
api_id = 27723896
api_hash = '5e40d3c33c3ef5e6b4ad03d70382ee5e'
session_name = "my_userbot"

# Создаем клиента Pyrogram
app = Client(session_name, api_id=api_id, api_hash=api_hash)

@app.on_message(filters.command("start", prefixes=".") & filters.me)
async def starter(client, message):
    await message.edit("Hello world!")

# Запуск клиента
app.run()