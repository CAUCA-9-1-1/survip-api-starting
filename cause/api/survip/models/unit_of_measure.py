from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent

Base = declarative_base()


class UnitOfMeasure(Base):
	__tablename__ = "tbl_unit_of_measure"

	id_unit_of_measure = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	abbreviation = Column(String(5))
	type = Column(String(20))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_unit_of_measure, id_language_content, abbreviation, type):
		self.id_unit_of_measure = id_unit_of_measure
		self.id_language_content_name = id_language_content
		self.abbreviation = abbreviation
		self.type = type
