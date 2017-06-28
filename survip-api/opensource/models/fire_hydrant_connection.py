from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .fire_hydrant import FireHydrant


Base = declarative_base()


class FireHydrantConnection(Base):
	__tablename__ = "tbl_fire_hydrant_connection"

	id_fire_hydrant_connection = Column(String(36), primary_key=True)
	id_fire_hydrant = Column(String(36), ForeignKey(FireHydrant.id_fire_hydrant), nullable=False)
	diameter = Column(Float)
	id_unit_of_measure_diameter = Column(String(36))
	id_fire_hydrant_connection_type = Column(String(36))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_fire_hydrant_connection, id_fire_hydrant, diameter, id_unit_of_measure, id_fire_hydrant_connection_type):
		self.id_fire_hydrant_connection = id_fire_hydrant_connection
		self.id_fire_hydrant = id_fire_hydrant
		self.diameter = diameter
		self.id_unit_of_measure_diameter = id_unit_of_measure
		self.id_fire_hydrant_connection_type = id_fire_hydrant_connection_type
