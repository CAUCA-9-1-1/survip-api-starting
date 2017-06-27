import json
from datetime import datetime
from geoalchemy2 import Geometry, functions
from sqlalchemy import Column, Boolean, DateTime, Float, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.database import Database
from .lane import Lane
from .intersection import Intersection
from .fire_hydrant_type import FireHydrantType


Base = declarative_base()


class FireHydrant(Base):
	__tablename__ = "tbl_fire_hydrant"

	id_fire_hydrant = Column(String(36), primary_key=True)
	id_lane = Column(String(36), ForeignKey(Lane.id_lane))
	id_intersection = Column(String(36), ForeignKey(Intersection.id_intersection))
	id_fire_hydrant_type = Column(String(36), ForeignKey(FireHydrantType.id_fire_hydrant_type))
	coordinates = Column(Geometry())
	altitude = Column(Float)
	fire_hydrant_number = Column(String(10))
	id_operator_type_rate = Column(String(36))
	id_unit_of_measure_rate = Column(String(36))
	rate_from = Column(String(5))
	rate_to = Column(String(5))
	id_operator_type_pressure = Column(String(36))
	id_unit_of_measure_pressure = Column(String(36))
	pressure_from = Column(String(5))
	pressure_to = Column(String(5))
	color = Column(String(50))
	physical_position = Column(String(50))
	comments = Column(Text)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def geojson(self):
		with Database() as db:
			points = db.query(functions.ST_AsGeoJSON(self.coordinates)).first()

		geojson = ()
		for pos, val in enumerate(points):
			geojson = geojson + (json.loads(val),)

		return geojson

	def __init__(self, id_fire_hydrant, id_fire_hydrant_type, fire_hydrant_number, id_lane, id_intersection):
		self.id_fire_hydrant = id_fire_hydrant
		self.id_fire_hydrant_type = id_fire_hydrant_type
		self.fire_hydrant_number = fire_hydrant_number
		self.id_lane = id_lane
		self.id_intersection = id_intersection

