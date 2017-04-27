import uuid
import logging
from .. import config
from .mysql import DbMysql
from .postgresql import DbPostgresql


class DB:
	db = None
	type = 'mysql'
	dbname = ''

	def __init__(self, db='general'):
		self.dbname = db

		if config.DATABASE is not None:
			if self.dbname in config.DATABASE:
				if 'type' in config.DATABASE[self.dbname]:
					self.type = config.DATABASE[self.dbname]['type']

				if self.type == 'postgresql' or self.type == 'pgsql':
					self.db = DbPostgresql(self.dbname)
				else:
					self.db = DbMysql(self.dbname)
			else:
				logging.exception("The DB: %s is not available" % self.dbname)
		else:
			logging.exception("The DB: %s is not available" % self.dbname)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.close()

	def commit(self):
		self.db.commit()

	def convert_args_for_right_db(self, args):
		convertArgs = ()

		if args is not None and self.type == 'mysql':
			for value in args:
				if isinstance(value, bool):
					convertArgs += ('1' if value is True else '0',)
				elif isinstance(value, uuid.UUID):
					convertArgs += (str(value),)
				else:
					convertArgs += (value,)
		elif args is not None and (self.type == 'postgresql' or self.type == 'pgsql'):
			for value in args:
				if isinstance(value, uuid.UUID):
					convertArgs += (str(value),)
				else:
					convertArgs += (value,)
		else:
			convertArgs = args

		return convertArgs

	def convert_query_for_right_db(self, query):
		if self.type == 'mysql':
			# Remove casting
			query = query.replace('::UUID', '').replace('::TEXT', '')
			query = query.replace('uuid_generate_v4()', "'%s'" % str(uuid.uuid4()))
		elif self.type == 'postgresql' or self.type == 'pgsql':
			pass

		return query

	def execute(self, query, args=None, commit=True):
		return self.db.execute(self.convert_query_for_right_db(query), self.convert_args_for_right_db(args), commit)

	def get(self, query, args=None):
		return self.db.get(self.convert_query_for_right_db(query), self.convert_args_for_right_db(args))

	def get_all(self, query, args=None, params=None):
		return self.db.get_all(self.convert_query_for_right_db(query), self.convert_args_for_right_db(args), params)

	def get_row(self, query, args=None):
		return self.db.get_row(self.convert_query_for_right_db(query), self.convert_args_for_right_db(args))

	def get_first(self, query, args=None):
		return self.db.get_first(self.convert_query_for_right_db(query), self.convert_args_for_right_db(args))

	def get_field(self, table_name):
		fields = []

		if self.type == 'mysql':
			field_name = 'Field'
			rows = self.db.get_all(self.convert_query_for_right_db("SHOW COLUMNS FROM %s;" % table_name))
		elif self.type == 'postgresql' or self.type == 'pgsql':
			field_name = 'attname'
			rows = self.db.get_all(
				self.convert_query_for_right_db("""SELECT a.attname
								FROM pg_catalog.pg_attribute a
								WHERE a.attnum > 0 AND NOT a.attisdropped AND a.attrelid = (
									SELECT c.oid FROM pg_catalog.pg_class c
									LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
									WHERE c.relname ~ '^(%s)$' AND pg_catalog.pg_table_is_visible(c.oid)
								);""" % table_name),
			)

		for row in rows:
			fields.append(row[field_name])

		return fields