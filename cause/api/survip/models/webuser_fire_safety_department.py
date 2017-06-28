from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from cause.api.management.models.webuser import Webuser
from .fire_safety_department import FireSafetyDepartment


Base = declarative_base()


class WebuserFireSafetyDepartment(Base):
	__tablename__ = "tbl_webuser_fire_safety_department"

	id_webuser_fire_safety_department = Column(String(36), primary_key=True)
	id_webuser = Column(String(36), ForeignKey(Webuser.id_webuser), nullable=False)
	id_fire_safety_department = Column(String(36), ForeignKey(FireSafetyDepartment.id_fire_safety_department), nullable=False)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_webuser_fire_safety_department, id_webuser, id_fire_safety_department):
		self.id_webuser_fire_safety_department = id_webuser_fire_safety_department
		self.id_webuser = id_webuser
		self.id_fire_safety_department = id_fire_safety_department
