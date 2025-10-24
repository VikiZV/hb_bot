import telebot
import requests
from datetime import datetime
from config import TOKEN_TG, OPENROUTER_API_KEY
from db import DB

"""Инициализация подключения к базе данных"""
db = DB(
    host='server102.hosting.reg.ru', user='u1450880_evg',
    password='aD6nK7hV7obJ4vB9', database='u1450880_evg'
    )

db.connect()

"""Инициализация Telegram бота"""
bot = telebot.TeleBot(TOKEN_TG)
ADMIN_ID = 836398223


def check_birthdays():
    """
    Функция проверки дней рождения.
    1. Получает текущую дату.
    2. Проверяет базу данных на совпадения по дате рождения (игнорируя год).
    3. Для каждого найденного имени генерирует поздравление через OpenRouter API.
    4. Отправляет сгенерированное поздравление админу в Telegram.
    """
    today = datetime.today().strftime("%Y-%m-%d")
    try:
        with db.connection.cursor() as cursor:
            cursor.execute("SELECT name FROM hb WHERE date_birth LIKE %s", (f"%{today[5:]}%",))
            result = cursor.fetchall()
            for row in result:
                name = row[0]

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Сгенерируй короткое поздравление с днем рождения для {name}. Только текст поздравления, без вариантов, без объяснений и комментариев, не добавляй никакой маркировки, только сам текст."
                        }
                    ],
                }
            )
            if response.status_code == 200:
                text = response.json()["choices"][0]["message"][
                    "content"]
                bot.send_message(ADMIN_ID,
                                 f"🎉 Поздравляем {name}!\n\n{text}")
            else:
                print("Ошибка генерации поздравления:", response.text)

    except Exception as e:
        print(f"Ошибка при проверке дней рождения: {e}")


check_birthdays()

# Чтобы бот отвечал и на команды тоже
@bot.message_handler(commands=['start'])
def start_handler(message):
    """
    Функция-обработчик команды /start.
    Отправляет приветственное сообщение при запуске бота пользователем.
    """
    bot.reply_to(message, "Бот запущен! 🎂")


bot.polling()


