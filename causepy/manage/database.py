from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, load_only
from causepy.config import setup as config


class Database:
	db = None
	metadata = None

	def __init__(self, db_name='general'):
		engine = create_engine('%s://%s:%s@%s/%s' % (
			config.DATABASE[db_name]['engine'],
			config.DATABASE[db_name]['username'],
			config.DATABASE[db_name]['password'],
			config.DATABASE[db_name]['host'],
			config.DATABASE[db_name]['dbname'],
		))
		session = sessionmaker()
		session.configure(bind=engine)

		self.db = session()
		self.metadata = MetaData(bind=engine)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.expunge_all()
		self.db.close()

	def query(self, *args):
		return self.db.query(*args)

	def select(self, class_table, fields):
		query = self.db.query(class_table)
		query.options(*fields)

		return query

	def add(self, item):
		self.db.add(item)

		return True

	def commit(self):
		self.db.commit()

		return True