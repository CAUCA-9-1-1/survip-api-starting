from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent


Base = declarative_base()


class UtilisationCode(Base):
	__tablename__ = "tbl_utilisation_code"

	id_utilisation_code = Column(String(36), primary_key=True)
	id_language_content_description = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	cubf = Column(String(5))
	scian = Column(String(10))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_description)

	def __init__(self, id_utilisation_code, id_language_content, cubf, scian):
		self.id_utilisation_code = id_utilisation_code
		self.id_language_content_description = id_language_content
		self.cubf = cubf
		self.scian = scian