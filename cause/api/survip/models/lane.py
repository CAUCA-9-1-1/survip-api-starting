from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from cause.api.management.core.manage.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent
from ..models.lane_generic_code import LaneGenericCode
from ..models.lane_public_code import LanePublicCode


Base = declarative_base()


class Lane(Base):
	__tablename__ = "tbl_lane"

	id_lane = Column(String(36), primary_key=True, nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_city = Column(String(36))
	public_lane_code = Column(String(50), ForeignKey(LanePublicCode.code))
	generic_code = Column(String(50), ForeignKey(LaneGenericCode.code))
	created_on = Column(DateTime, default=datetime.now)
	is_valid = Column(Boolean, default=False)
	is_active = Column(Boolean, default=True)

	lane_generic_code = relationship(LaneGenericCode)
	lane_public_code = relationship(LanePublicCode)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_lane, id_language_content, id_city, public_lane_code, generic_code):
		self.id_lane = id_lane
		self.id_language_content_name = id_language_content
		self.id_city = id_city
		self.public_lane_code = public_lane_code
		self.generic_code = generic_code
