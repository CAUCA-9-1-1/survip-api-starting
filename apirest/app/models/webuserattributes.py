from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


Base = declarative_base()


class WebuserAttributes(Base):
	__tablename__ = "tbl_webuser_attributes"

	id_webuser = Column(String(36), primary_key=True)
	attribute_name = Column(String(50), primary_key=True)
	attribute_value = Column(String(200))
