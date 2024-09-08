from pyrogram import Client, filters
import requests

# Ваш API ID, API Hash и session name
api_id = 27723896
api_hash = '5e40d3c33c3ef5e6b4ad03d70382ee5e'
session_name = "my_userbot"

# Инициализация клиента Pyrogram
app = Client(session_name, api_id=api_id, api_hash=api_hash)

# Словарь для хранения последних сообщений от пользователей
user_messages = {}

# Инициализация глобальных данных
system_description = "Ты ИИ помощница с именем Пятница."
owner_name = "кьюасар"

# Функция для отправки сообщения к Groq API
def send_to_groq(messages, system_message):
    prompt = [{"role": "system", "content": system_message}]
    for message in messages[-10:]:
        prompt.append({"role": "user", "content": message})
    
    # Отправка запроса к Groq
    response = requests.post("https://api.groq.com/v1/chat/completions", 
                             headers={"Authorization": "Bearer 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"},
                             json={"messages": prompt})
    response_data = response.json()
    return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

# Обработка сообщений от пользователей
@app.on_message(filters.private & ~filters.me)
async def handle_message(client, message):
    global user_messages

    user_id = message.from_user.id
    user_text = message.text

    # Инициализация истории сообщений для нового пользователя
    if user_id not in user_messages:
        user_messages[user_id] = []

    # Добавление нового сообщения в историю
    user_messages[user_id].append(user_text)
    
    # Проверка на изменение настроек бота (например, смена имени и т.д.)
    if "запомни" in user_text.lower():
        # Пример изменения системного сообщения
        system_description += f" Remember that: {user_text.split('запомни', 1)[1].strip()}."
    elif "поменяй имя" in user_text.lower():
        owner_name = user_text.split("поменяй имя", 1)[1].strip()
        system_description += f" Now, the owner is known as {owner_name}."
    elif "назови свое имя" in user_text.lower():
        await message.reply_text(f"Меня зовут {owner_name}.")
        return
    elif "обнови описание" in user_text.lower():
        # Обновление описания
        system_description += f" Describe your owner: {owner_name} likes to talk about various topics."
        await message.reply_text("Описание обновлено.")
        return

    # Формирование сообщения для отправки к Groq
    response_text = send_to_groq(user_messages[user_id], system_description)

    # Ответ пользователю
    await message.reply_text(response_text)

if __name__ == "__main__":
    app.run()