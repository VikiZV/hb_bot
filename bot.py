"""
Telegram бот для поздравления с днем рождения.

Бот проверяет базу данных на совпадения с текущей датой (без учета года),
генерирует поздравления через OpenRouter API и отправляет их администратору.
Также поддерживает команду /add для добавления новых пользователей в базу данных.
"""

import re
import json
import telebot
import requests
from datetime import datetime
from config import (
    TOKEN_TG,
    OPENROUTER_API_KEY,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    ADMIN_ID,
)
from db import DB

# Константа URL для OpenRouter API
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Инициализация подключения к базе данных
db = DB(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)
db.connect()

# Инициализация Telegram бота
bot = telebot.TeleBot(TOKEN_TG)


def check_birthdays() -> None:
    """
    Проверяет наличие дней рождения на текущую дату и отправляет поздравления.
    1. Для каждого найденного имени генерирует поздравление через OpenRouter API
       с таймаутом и обработкой ошибок.
    """
    today = datetime.today().strftime("%Y-%m-%d")
    try:
        with db.connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM hb WHERE DATE_FORMAT(date_birth, '%m-%d') = %s",
                (today[5:],)
            )
            result = cursor.fetchall()
            print(f"Сегодня: {today}, найдено {len(result)} имен для поздравления")

            for row in result:
                name = row[0]

                try:
                    response = requests.post(
                        url=OPENROUTER_URL,
                        headers={
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        data=json.dumps({
                            "model": "qwen/qwen3-coder:free",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": (
                                        f"Сгенерируй короткое поздравление с днем рождения для {name}. "
                                        "Только текст поздравления, без вариантов, без объяснений и комментариев, "
                                        "не добавляй никакой маркировки, только сам текст."
                                    ),
                                }
                            ],
                        }),
                        timeout=15
                    )

                    response.raise_for_status()

                    text = response.json()["choices"][0]["message"]["content"]

                    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

                    bot.send_message(ADMIN_ID, f"🎉 Поздравляем {name}!\n\n{text}")

                except requests.exceptions.RequestException as e:
                    print(f"Ошибка запроса к OpenRouter для {name}: {e}")

                except KeyError:
                    print(f"Не удалось получить текст поздравления для {name} из ответа API.")

    except Exception as e:
        print(f"Ошибка при проверке дней рождения: {e}")


@bot.message_handler(commands=["start"])
def start_handler(message) -> None:
    """
    Функция-обработчик команды /start.
    Отправляет приветственное сообщение при запуске бота пользователем.
    """
    bot.reply_to(message, "Бот запущен! 🎂")


if __name__ == "__main__":
    check_birthdays()
    bot.polling()