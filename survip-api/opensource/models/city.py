from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.multilang import MultiLang
from framework.models.language_content import LanguageContent
from .county import County


Base = declarative_base()


class City(Base):
	__tablename__ = "tbl_city"

	id_city = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_county = Column(String(36), ForeignKey(County.id_county))
	code = Column(String(5))
	code3_letter = Column(String(3))
	email_address = Column(String(100))
	created_on = Column(DateTime, default=datetime.now())
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_city, id_language_content, id_county, code, code3_letter, email_address):
		self.id_city = id_city
		self.id_language_content_name = id_language_content
		self.id_county = id_county
		self.code = code
		self.code3_letter = code3_letter
		self.email_address = email_address
