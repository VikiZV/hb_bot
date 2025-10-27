"""
main.py — Точка входа Telegram-бота.
Запускает основные функции и инициализирует обработчики команд.
"""
from bot import bot, check_birthdays

if __name__ == '__main__':
	print('Бот запустился...')
	check_birthdays()
	try:
		bot.infinity_polling()
	except KeyboardInterrupt:
		print("Bot stopped by user.")
	except Exception as e:
		print(f"Unexpected error: {e}")

