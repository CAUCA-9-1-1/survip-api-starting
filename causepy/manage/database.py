import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from causepy.config import setup as config


class Database:
	engine = None
	session = None
	metadata = None

	def __init__(self, db_name='general'):
		if 'username' in config.DATABASE[db_name]:
			self.engine = create_engine('%s://%s:%s@%s/%s' % (
				config.DATABASE[db_name]['engine'],
				config.DATABASE[db_name]['username'],
				config.DATABASE[db_name]['password'],
				config.DATABASE[db_name]['host'],
				config.DATABASE[db_name]['dbname'],
			), echo=config.IS_DEV)
		else:
			self.engine = create_engine('%s:///%s' % (
				config.DATABASE[db_name]['engine'],
				config.DATABASE[db_name]['dbname'],
			), echo=config.IS_DEV)

		Session = sessionmaker()
		Session.configure(bind=self.engine)

		self.session = Session()
		self.metadata = MetaData(bind=self.engine)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.session.expunge_all()
		self.session.close()

	def query(self, *args):
		return self.session.query(*args)

	def insert(self, item):
		self.session.add(item)

		return True

	def commit(self):
		self.session.commit()

		return True