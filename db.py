import pymysql

class DB:
	def __init__(self, host, user, password, database):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.connection = None

	"""Соединение с db"""
	def connect(self):
		try:
			self.connection = pymysql.connect(
				host=self.host,
				user=self.user,
				password=self.password,
				database=self.database,
			)
			print('Соединение установлено')
		except Exception as e:
			print(f'Ошибка соединения {e}')

	"""Добавление данных о пользователе"""
	def add_person(self, id, name, date_birth):
		sql = '''INSERT INTO hb (id, name, date_birth) VALUES (%s, %s, %s)'''
		values = (id, name, date_birth)
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(sql, values)
			self.connection.commit()
			print('Данные добавлены')
		except Exception as e:
			print(f'Ошибка добавления данных {e}')

	"""Редактирование данных о пользователе"""
	def update_person_date(self, id, name, date_birth):
		sql = '''UPDATE hb SET date_birth = %s WHERE id = %s AND name = %s'''
		values = (date_birth, id, name)
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(sql, values)
			self.connection.commit()
			print('Данные обновлены')
		except Exception as e:
			print(f'Ошибка обновления данных {e}')


if __name__ == '__main__':
	db = DB(host='server102.hosting.reg.ru', user='u1450880_evg',
		password='aD6nK7hV7obJ4vB9', database='u1450880_evg')
	db.connect()
	db.add_person(7, 'Мартин', '2025-10-24')
