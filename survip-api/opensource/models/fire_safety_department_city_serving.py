from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .city import City
from .fire_safety_department import FireSafetyDepartment


Base = declarative_base()


class FireSafetyDepartmentCityServing(Base):
	__tablename__ = "tbl_fire_safety_department_city_serving"

	id_fire_safety_department_city_serving = Column(String(36), primary_key=True)
	id_fire_safety_department = Column(String(36), ForeignKey(FireSafetyDepartment.id_fire_safety_department), nullable=False)
	id_city = Column(String(36), ForeignKey(City.id_city))
	id_sector_type = Column(String(36))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_fire_safety_department_city_serving, id_fire_safety_department, id_city):
		self.id_fire_safety_department_city_serving = id_fire_safety_department_city_serving
		self.id_fire_safety_department = id_fire_safety_department
		self.id_city = id_city
