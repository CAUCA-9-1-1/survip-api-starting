from datetime import datetime
from framework.manage.multilang import MultiLang
from framework.models.language_content import LanguageContent
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Lane(Base):
	__tablename__ = "tbl_lane"

	id_lane = Column(String(36), primary_key=True, nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_city = Column(String(36))
	public_lane_code = Column(String(50))
	generic_code = Column(String(50))
	created_on = Column(DateTime, default=datetime.now)
	is_valid = Column(Boolean, default=False)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_lane, id_language_content, id_city):
		self.id_lane = id_lane
		self.id_language_content_name = id_language_content
		self.id_city = id_city
