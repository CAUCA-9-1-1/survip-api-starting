import json
from datetime import datetime
from geoalchemy2 import Geometry, functions
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.database import Database
from .lane import Lane


Base = declarative_base()


class Intersection(Base):
	__tablename__ = "tbl_intersection"

	id_intersection = Column(String(36), primary_key=True, nullable=False)
	id_lane = Column(String(36), ForeignKey(Lane.id_lane))
	id_lane_transversal = Column(String(36), ForeignKey(Lane.id_lane))
	id_fire_sector = Column(String(36))
	id_jaws_sector = Column(String(36))
	id_mutual_aid_sector = Column(String(36))
	id_rescue_sector = Column(String(36))
	id_fire_sub_sector = Column(String(36))
	coordinates = Column(Geometry())
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

	def __init__(self, id_intersection, id_lane, id_lane_transversal):
		self.id_intersection = id_intersection
		self.id_lane = id_lane
		self.id_lane_transversal = id_lane_transversal

