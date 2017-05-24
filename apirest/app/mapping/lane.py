from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from causepy.mapping.language_content import LanguageContent


Base = declarative_base()


class Lane(Base):
	__tablename__ = "tbl_lane"

	id_lane = Column(String(36), primary_key=True, nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_city = Column(String(36))
	public_lane_code = Column(String(50))
	generic_code = Column(String(50))
	created_on = Column(DateTime)
	is_valid = Column(Boolean)
	is_active = Column(Boolean)

	name = relationship(LanguageContent, lazy='joined')
