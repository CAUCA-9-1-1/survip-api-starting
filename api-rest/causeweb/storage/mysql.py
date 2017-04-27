import logging

try:
	import mysql.connector
except:
	pass

from .. import config


class DbMysql:
	cnx = None
	dbname = ''

	def __init__(self, db='general'):
		""" Initialize the database connection

		:param dbname: DB to use
		"""
		self.cnx = None
		self.dbname = db
		self.connected = False

		if config.DATABASE is not None:
			if self.dbname in config.DATABASE:
				try:
					self.cnx = mysql.connector.connect(
									user=config.DATABASE[self.dbname]['username'],
									password=config.DATABASE[self.dbname]['password'],
					                database=config.DATABASE[self.dbname]['dbname'],
									host=config.DATABASE[self.dbname]['host'])
				except Exception as e:
					raise Exception('Error during connection to mysql DB')

				if self.cnx is not None:
					self.connected = True
				else:
					raise Exception("We can't connect to this DB : %s" % config.DATABASE[self.dbname]['dbname'])
			else:
				raise Exception("The DB: %s is not available" % self.dbname)
		else:
			raise Exception("The DB: %s is not available" % self.dbname)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def close(self):
		""" Close the database connection
		"""
		if self.cnx is not None:
			self.cnx.close()

	def commit(self):
		""" Commit the change on database
		"""
		self.cnx.commit()

	def execute(self, query, args=None, commit=True):
		""" Run a query on dababase

		:param query: Query to run
		:param commit: Force to commit the change
		"""
		if self.cnx is not None:
			cursor = self.cnx.cursor(buffered=True)

			try:
				if args is None:
					cursor.execute(query)
				else:
					cursor.execute(query, args)

				if commit is True:
					self.cnx.commit()
			except mysql.connector.Error as e:
				if self.cnx:
					self.cnx.rollback()

					raise Exception('query: %s, args: %s, error: %s' % (query, args, e))
			except Exception as e:
				raise Exception('Error is not on query : %s' % e)
			finally:
				cursor.close()
		else:
			raise Exception("We can't connect to this DB")

	def get(self, query, args=None):
		""" Select first field of first row

		:param query: Query to run
		:return: Value of field
		"""
		result = ''

		if self.cnx is not None:
			cursor = self.cnx.cursor(buffered=True)

			try:
				cursor.execute(query, args)
				row = cursor.fetchone()

				if row is not None:
					result = row[0]

				cursor.close()
			except mysql.connector.Error as e:
				raise Exception('query: %s, args: %s, error: %s' % (query, args, e))
			except Exception as e:
				raise Exception('Error is not on query : %s' % e)
		else:
			raise Exception("We can't connect to this DB")

		return result

	def get_all(self, query, args=None, params=None):
		""" Select each field and row

		:param query: Query to run
		:return: dict with all field and row
		"""
		result = list()

		if self.cnx is not None:
			cursor = self.cnx.cursor(buffered=True)

			try:
				if params is not None:
					cursor.callproc(query, params)

					for results in cursor.stored_results():
						fields = [i[0] for i in results.description]
						rows = results.fetchall()
				else:
					if args is None:
						cursor.execute(query)
					else:
						cursor.execute(query, args)

					rows = cursor.fetchall()

					if rows is not None:
						fields = [i[0] for i in cursor.description]

				if rows is not None:
					for row in rows:
						my_row = dict()
						for i in range(len(fields)):
							my_row.update({fields[i]: row[i]})
						result.append(my_row)

				cursor.close()
			except mysql.connector.Error as e:
				raise Exception('query: %s, args: %s, error: %s' % (query, args, e))
			except Exception as e:
				raise Exception('Error is not on query : %s' % e)
		else:
			raise Exception("We can't connect to this DB")

		return result

	def get_row(self, query, args=None):
		""" Select first row

		:param query: Query ro tun
		:return: dict with first row
		"""
		result = dict()

		if self.cnx is not None:
			cursor = self.cnx.cursor(buffered=True)

			try:
				if args is None:
					cursor.execute(query)
				else:
					cursor.execute(query, args)

				fields = [i[0] for i in cursor.description]
				row = cursor.fetchone()

				if row is not None:
					for i in range(len(fields)):
						result.update({fields[i]: row[i]})

				cursor.close()
			except mysql.connector.Error as e:
				raise Exception('query: %s, args: %s, error: %s' % (query, args, e))
			except Exception as e:
				raise Exception('Error is not on query : %s' % e)
		else:
			raise Exception("We can't connect to this DB")

		return result

	def get_first(self, query, args=None):
		""" Select first field of each row

		:param query: Query ro tun
		:return: dict with first field of each row
		"""
		result = list()

		if self.cnx is not None:
			cursor = self.cnx.cursor(buffered=True)

			try:
				if args is None:
					cursor.execute(query)
				else:
					cursor.execute(query, args)

				rows = cursor.fetchall()
				cursor.close()

				if rows is not None:
					for row in rows:
						result.append(row[0])

				cursor.close()
			except mysql.connector.Error as e:
				raise Exception('query: %s, args: %s, error: %s' % (query, args, e))
			except Exception as e:
				raise Exception('Error is not on query : %s' % e)
		else:
			raise Exception("We can't connect to this DB")

		return result
