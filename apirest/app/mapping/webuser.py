from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, DateTime, String

Base = declarative_base()


class Webuser(Base):
	__tablename__ = "tbl_webuser"

	id_webuser = Column(String(36), primary_key=True)
	username = Column(String(100))
	password = Column(String(100))
	created_on = Column(DateTime)
	is_active = Column(Boolean)
