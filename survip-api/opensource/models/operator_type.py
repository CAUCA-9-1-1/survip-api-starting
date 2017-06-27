from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OperatorType(Base):
	__tablename__ = "tbl_operator_type"

	id_operator_type = Column(String(36), primary_key=True)
	symbol = Column(String(3), nullable=False)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_operator_type, symbol):
		self.id_operator_type = id_operator_type
		self.symbol = symbol
