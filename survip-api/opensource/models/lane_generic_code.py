from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean

Base = declarative_base()


class LaneGenericCode(Base):
	__tablename__ = "tbl_lane_generic_code"

	code = Column(String(1), primary_key=True)
	description = Column(String(15))
	add_white_space_after = Column(Boolean)
	is_active = Column(Boolean)

	def __init__(self, code, description, add_white_space_after, is_active):
		self.code = code
		self.description = description
		self.add_white_space_after = add_white_space_after
		self.is_active = is_active