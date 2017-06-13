from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.multilang import MultiLang
from framework.models.language_content import LanguageContent


Base = declarative_base()


class UtilisationCode(Base):
	__tablename__ = "tbl_utilisation_code"

	id_utilisation_code = Column(String(36), primary_key=True)
	id_language_content_description = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	cubf = Column(String(5))
	scian = Column(String(10))
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_description)