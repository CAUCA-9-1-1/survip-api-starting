from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean

Base = declarative_base()


class LanePublicCode(Base):
	__tablename__ = "tbl_lane_public_code"

	code = Column(String(2), primary_key=True)
	description = Column(String(20))
	abbreviation = Column(String(2))
	is_active = Column(Boolean)

	def __init__(self, code, description, abbreviation, is_active):
		self.code = code
		self.description = description
		self.abbreviation = abbreviation
		self.is_active = is_active