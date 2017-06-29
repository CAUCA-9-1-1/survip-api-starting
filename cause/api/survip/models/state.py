from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent
from .country import Country


Base = declarative_base()


class State(Base):
	__tablename__ = "tbl_state"

	id_state = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_country = Column(String(36), ForeignKey(Country.id_country))
	ansi_code = Column(String(2))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_state, id_language_content, id_country, ansi_code):
		self.id_state = id_state
		self.id_language_content_name = id_language_content
		self.id_country = id_country
		self.ansi_code = ansi_code