from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, DateTime, String

Base = declarative_base()


class Country(Base):
	__tablename__ = "tbl_country"

	id_country = Column(String(36), primary_key=True)
	code_alpha2 = Column(String(2))
	code_alpha3 = Column(String(3))
	created_on = Column(DateTime)
	is_active = Column(Boolean)
