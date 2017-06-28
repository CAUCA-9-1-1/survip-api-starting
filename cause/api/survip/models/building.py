import json
from datetime import datetime

from geoalchemy2 import Geometry, functions
from sqlalchemy import Column, Boolean, DateTime, Float, Numeric, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from api.management.core.database import Database
from api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent
from .lane import Lane

Base = declarative_base()


class Building(Base):
	__tablename__ = "tbl_building"

	id_building = Column(String(26), primary_key=True, nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	matricule = Column(String(18), nullable=False)
	civic_number = Column(String(15))
	id_lane = Column(String(36), nullable=False)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	@hybrid_property
	def address(self):
		with Database() as db:
			lane = db.query(Lane).get(self.id_lane)

		return self.civic_number + ', ' + lane.name['fr']

	def __init__(self, id_building, id_language_content, civic_number):
		self.id_building = id_building
		self.id_language_content_name = id_language_content
		self.civic_number = civic_number


class BuildingFull(Building):
	civic_letter = Column(String(10))
	civic_supp = Column(String(10))
	civic_letter_supp = Column(String(10))
	appartment_number = Column(String(10))
	floor = Column(String(10))
	suite = Column(String(Numeric))
	number_of_appartment = Column(Numeric)
	number_of_building = Column(Numeric)
	vacant_land = Column(Boolean)
	year_of_construction = Column(Numeric)
	building_value = Column(Float)
	postal_code = Column(String(6))
	id_utilisation_code = Column(String(36))
	id_sector = Column(String(36))
	id_mutual_aid_sector = Column(String(36))
	id_jaws_extrication_sector = Column(String(36))
	id_sled_sector = Column(String(36))
	source = Column(String(25))
	is_parent = Column(Boolean)
	utilisation_description = Column(String(255))
	show_in_resources = Column(Boolean)
	id_resource_category = Column(String(50))
	id_association_building = Column(String(50))
	id_association_type = Column(String(50))
	id_unit_type = Column(String(50))
	coordinates = Column(Geometry())
	coordinates_source = Column(String(50))
	details = Column(Text)

	@hybrid_property
	def geojson(self):
		with Database() as db:
			points = db.query(functions.ST_AsGeoJSON(self.coordinates)).first()

		geojson = ()
		for pos, val in enumerate(points):
			geojson = geojson + (json.loads(val),)

		return geojson
