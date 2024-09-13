import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# Ваш API ID, API Hash и session name
api_id = 27723896
api_hash = '5e40d3c33c3ef5e6b4ad03d70382ee5e'
session_name = "my_userbot"

app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Функция для удаления всех сообщений пользователя
async def delete_all_messages(client, message):
    user_id = message.from_user.id
    total_deleted = 0
    status_message = await message.reply(f"Количество сообщений: {total_deleted}\nСтатус: В процессе")

    async for msg in app.search_messages(message.chat.id, from_user=user_id):
        try:
            await msg.delete()
            total_deleted += 1
            await status_message.edit(f"Количество сообщений: {total_deleted}\nСтатус: В процессе")
        except FloodWait as e:
            await asyncio.sleep(e.x)  # Ожидание, чтобы не было блокировки за флуд
        except Exception as e:
            await status_message.edit(f"Количество сообщений: {total_deleted}\nСтатус: Ошибка")
            return

    await status_message.edit(f"Количество сообщений: {total_deleted}\nСтатус: Удалено")


@app.on_message(filters.me & filters.command("clearall", prefixes="."))
async def clear_all_messages(client, message):
    await delete_all_messages(client, message)


app.run()