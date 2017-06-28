from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.multilang import MultiLang
from framework.models.language_content import LanguageContent


Base = declarative_base()


class FireHydrantConnectionType(Base):
	__tablename__ = "tbl_fire_hydrant_connection_type"

	id_fire_hydrant_connection_type = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_fire_hydrant_connection_type, id_language_content):
		self.id_fire_hydrant_connection_type = id_fire_hydrant_connection_type
		self.id_language_content_name = id_language_content
