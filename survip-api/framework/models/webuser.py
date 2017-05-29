from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, DateTime, String
from ..auth.encryption import Encryption


Base = declarative_base()


class Webuser(Base):
	__tablename__ = "tbl_webuser"

	id_webuser = Column(String(36), primary_key=True)
	username = Column(String(100))
	password = Column(String(100))
	created_on = Column(DateTime, default=datetime.now())
	is_active = Column(Boolean, default=True)

	def __init__(self, id_webuser, username, password):
		self.id_webuser = id_webuser
		self.username = username
		self.password = Encryption.password(password)