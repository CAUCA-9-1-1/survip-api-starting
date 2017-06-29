from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent


Base = declarative_base()


class RiskLevel(Base):
	__tablename__ = "tbl_risk_level"

	id_risk_level = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	sequence = Column(Integer)
	code = Column(Integer)
	color = Column(String(10))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_risk_level, id_language_content, sequence, code, color):
		self.id_risk_level = id_risk_level
		self.id_language_content_name = id_language_content
		self.sequence = sequence
		self.code = code
		self.color = color