from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent


Base = declarative_base()


class PersonRequiringAssistanceType(Base):
	__tablename__ = "tbl_person_requiring_assistance_type"

	id_person_requiring_assistance_type = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_person_requiring_assistance_type, id_language_content):
		self.id_person_requiring_assistance_type = id_person_requiring_assistance_type
		self.id_language_content_name = id_language_content