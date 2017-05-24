from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class LanguageContent(Base):
	__tablename__ = "tbl_language_content"

	id_language_content = Column(String(36), primary_key=True)
	language_code = Column(String(5), primary_key=True)
	description = Column(String(250))
