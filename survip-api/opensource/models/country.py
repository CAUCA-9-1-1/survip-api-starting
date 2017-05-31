from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.multilang import MultiLang
from framework.models.language_content import LanguageContent


Base = declarative_base()


class Country(Base):
	__tablename__ = "tbl_country"

	id_country = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	code_alpha2 = Column(String(2))
	code_alpha3 = Column(String(3))
	created_on = Column(DateTime, default=datetime.now())
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)