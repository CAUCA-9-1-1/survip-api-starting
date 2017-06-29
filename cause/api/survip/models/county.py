from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent
from .region import Region
from .state import State


Base = declarative_base()


class County(Base):
	__tablename__ = "tbl_county"

	id_county = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_region = Column(String(36), ForeignKey(Region.id_region))
	id_state = Column(String(36), ForeignKey(State.id_state))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_county, id_language_content, id_region, id_state):
		self.id_county = id_county
		self.id_language_content_name = id_language_content
		self.id_region = id_region
		self.id_state = id_state